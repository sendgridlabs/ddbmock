# -*- coding: utf-8 -*-

from ddbmock.errors import ConditionalCheckFailedException, ValidationException
from ddbmock import config
from decimal import Decimal
from math import ceil
from . import comparison


def _decode_field(field):
    """
    Read a field's type and value

    :param field: Raw DynamoDB request field of the form ``{'typename':'value'}``

    :return: (typename, value) string tuple
    """
    return field.items()[0]

class ItemSize(int):
    """
    Utility class to represent an :py:class:`Item` size as bytes or capacity units
    """
    def __add__(self, value):
        """
        Transparently allow addition of ``ItemSize`` values. This is useful for
        all batch requests as ``Scan``, ``Query``, ``BatchWriteItem`` and
        ``BatchReadItem``

        :param value: foreign int compatible value to add

        :return: new :py:class:`ItemSize` value

        :raises: ``TypeError`` if ``value`` is not int compatible
        """
        return ItemSize(int.__add__(self, value))

    def as_units(self):
        """
        Get item size in terms of capacity units. This does *not* include the
        index overhead. Units can *not* be bellow 1 ie: a ``DeleteItem`` on a non
        existing item is *not* free

        :return: number of capacity unit consummed by any operation on this ``ItemSize``
        """
        return max(1, int(ceil((self) / 1024.0)))

    def with_indexing_overhead(self):
        """
        Take the indexing overhead into account. this is especially usefull
        to compute the table disk size as DynamoDB would but it's not included
        in the capacity unit calculation.

        :return: ``ItemSize`` + :py:const:`ddbmock.config.INDEX_OVERHEAD`
        """
        return self + config.INDEX_OVERHEAD


class Item(dict):
    """
    Internal Item representation. The Item is stored in its raw DynamoDB request
    form and no parsing is involved unless specifically needed.

    It adds a couple of handful helpers to the dict class such as DynamoDB actions,
    condition validations and specific size computation.
    """
    def __init__(self, dico={}):
        """
        Load a raw DynamoDb Item and enhance it with ou helpers. Also set the
        cached :py:class:`ItemSize` to ``None`` to mark it as not computed. This
        avoids unnecessary computations on temporary Items.

        :param dico: Raw DynamoDB request Item
        """
        self.update(dico)
        self.size = None

    def filter(self, fields):
        """
        Return a dict containing only the keys specified in ``fields``. If
        ``fields`` evaluates to False (None, empty, ...), the original dict is
        returned untouched.

        Internal :py:class:`ItemSize` of the filtered Item is set to original
        Item size as you pay for the data you operated on, not for what was
        actually sent over the wires.

        :param fields: array of name of keys to keep

        :return: filtered ``Item``
        """
        if fields:
            filtered = Item((k, v) for k, v in self.items() if k in fields)
            filtered.size = self.get_size()  # Filtered or not, you pay for actual size
            return filtered
        return self

    def _apply_action(self, fieldname, action):
        """
        Internal function. Applies a single action to a single field.

        :param fieldname: Valid field name
        :param action: Raw DynamoDB request action specification

        :raises: :py:exc:`ddbmock.errors.ValidationException` whenever attempting an illegual action
        """
        # Rewrite this function, it's disgustting code
        if action[u'Action'] == u"PUT":
            self[fieldname] = action[u'Value']

        if action[u'Action'] == u"DELETE": # Starts to be anoying
            if not fieldname in self:
                return  #shortcut
            if u'Value' not in action:
                del self[fieldname] # Nice and easy part
                return

            typename, value = _decode_field(action[u'Value'])
            ftypename, fvalue = _decode_field(self[fieldname])

            if len(ftypename) != 2:
                raise ValidationException(u"Can not DELETE elements from a non set type. Got {}".format(ftypename))
            if ftypename != typename:
                raise ValidationException(u"Expected type {t} for DELETE from type {t}. Got {}".format(typename, t=ftypename))

            # do the dirty work
            data = set(fvalue).difference(value)
            # if data empty => remove the key
            if not data:
                del self[fieldname]
            else:
                self[fieldname] = {ftypename: list(data)}

        if action[u'Action'] == u"ADD":  # Realy anoying to code :s
            #FIXME: not perfect, action should be different if the item was new
            typename, value = _decode_field(action[u'Value'])
            if fieldname in self:
                ftypename, fvalue = _decode_field(self[fieldname])

                if ftypename == u"N":
                    data = Decimal(value) + Decimal(fvalue)
                    self[fieldname][u"N"] = unicode(data)
                elif ftypename in [u"NS", u"SS", u"BS"]:
                    if ftypename != typename:
                        raise ValidationException(u"Expected type {t} for ADD in type {t}. Got {}".format(typename, t=ftypename))
                    data = set(fvalue).union(value)
                    self[fieldname][typename] = list(data)
                else:
                    raise ValidationException(u"Only N, NS, SS and BS types supports ADD operation. Got {}".format(ftypename))
            else:
                if typename not in [u"N", u"NS"]:
                    raise ValidationException(u"When performing ADD operation on new field, only Numbers or Numbers set are allowed. Got {} of type {}".format(value, typename))
                self[fieldname] = action[u'Value']

    def apply_actions(self, actions):
        """
        Apply ``actions`` to the current item. Mostly used by ``UpdateItem``.
        This also resets the cached item size.

        .. warning:: There is a corner case in ``ADD`` action. It will always behave
            as though the item already existed before that is to say, it the target
            field is a non existing set, it will always start a new one with this
            single value in it. In real DynamoDB, if Item was new, it should fail.

        :param action: Raw DynamoDB request actions specification

        :raises: :py:exc:`ddbmock.errors.ValidationException` whenever attempting an illegual action
        """
        map(self._apply_action, actions.keys(), actions.values())
        self.size = None  # reset cache

    def assert_match_expected(self, expected):
        """
        Make sure this Items matches the ``expected`` values. This may be used
        by any signe item write operation such as ``DeleteItem``, ``UpdateItem``
        and ``PutItem``.

        :param expected: Raw DynamoDB request expected values

        :raises: :py:exc:`ddbmock.errors.ConditionalCheckFailedException` if any of the expected values is not valid
        """
        for fieldname, condition in expected.iteritems():
            if u'Exists' in condition and not condition[u'Exists']:
                if fieldname in self:
                    raise ConditionalCheckFailedException(
                        "Field '{}' should not exist".format(fieldname))
                # *IS* executed but coverage bug
                continue  # pragma: no cover
            if fieldname not in self:
                raise ConditionalCheckFailedException(
                    "Field '{}' should exist".format(fieldname))
            if self[fieldname] != condition[u'Value']:
                raise ConditionalCheckFailedException(
                    "Expected field '{}'' = '{}'. Got '{}'".format(
                    fieldname, condition[u'Value'], self[fieldname]))

    def match(self, conditions):
        """
        Check if the current item matches conditions. Return False if a field is not
        found, or does not match. If condition is None, it is considered to match.

        Condition name are assumed to be valid as Onctuous is in charge of input
        validation. Expect crashes otherwise :)

        :param fieldname: Valid field name
        :param condition: Raw DynamoDB request condition of the form ``{"OPERATOR": FIELDDEFINITION}``

        :return: ``True`` on success or ``False`` on first failure
        """
        for name, condition in conditions.iteritems():
            if not self.field_match(name, condition):
                return False

        return True

    def field_match(self, fieldname, condition):
        """
        Check if a field matches a condition. Return False when field not
        found, or do not match. If condition is None, it is considered to match.

        Condition name are assumed to be valid as Onctuous is in charge of input
        validation. Expect crashes otherwise :)

        :param fieldname: Valid field name
        :param condition: Raw DynamoDB request condition of the form ``{"OPERATOR": FIELDDEFINITION}``

        :return: ``True`` on success
        """
        # Arcording to specif, no condition means match
        if condition is None:
            return True

        # read the item
        if fieldname not in self:
            value = None
        else:
            value = self[fieldname]

        # Load the test operator from the comparison module. Thanks to input
        # validation, no try/except required
        condition_operator = condition[u'ComparisonOperator'].lower()
        operator = getattr(comparison, condition_operator)
        return operator(value, *condition[u'AttributeValueList'])

    def read_key(self, key, name=None, max_size=0):
        """
        Provided ``key``, read field value at ``name`` or ``key.name`` if not
        specified.

        :param key: ``Key`` or ``PrimaryKey`` to read
        :param name: override name field of key
        :param max_size: if specified, check that the item is bellow a treshold

        :return: field value at ``key``

        :raises: :py:exc:`ddbmock.errors.ValidationException` if field does not exist, type does not match or is above ``max_size``
        """
        if key is None:
            return False
        if name is None:
            name = key.name

        try:
            field = self[name]
        except KeyError:
            raise ValidationException(u'Field {} not found'.format(name))

        if max_size:
            size = self.get_field_size(name)
            if size > max_size:
                raise ValidationException(u'Field {} is over {} bytes limit. Got {}'.format(name, max_size, size))

        return key.read(field)

    def _internal_item_size(self, base_type, value):
        """
        Internal DynamoDB field size computation. ``base_type`` is assumed to
        be valid as it went through Onctous before and this helper is only
        supposed to be called internally.

        :param base_type: valid base type. Must be in ``['N', 'S', 'B']``.
        :param value: compute the size of this value.
        """
        if base_type == 'N': return 8 # assumes "double" internal type on ddb side
        if base_type == 'S': return len(value.encode('utf-8'))
        if base_type == 'B': return len(value.encode('utf-8'))*3/4 # base64 overhead

    def get_field_size(self, fieldname):
        """
        Compute field size in bytes.

        :param fieldname: Valid field name

        :return: Size of the field in bytes or 0 if the field was not found. Remember that empty fields are represented as missing values in DynamoDB.
        """
        if not fieldname in self:
            return 0

        typename, value = _decode_field(self[fieldname])
        base_type = typename[0]

        if len(typename) == 1:
            value_size = self._internal_item_size(base_type, value)
        else:
            value_size = 0
            for v in value:
                value_size += self._internal_item_size(base_type, v)

        return value_size

    def get_size(self):
        """
        Compute Item size as DynamoDB would. This is especially useful for
        enforcing the 64kb per item limit as well as the capacityUnit cost.

        .. note:: the result is cached for efficiency. If you ever happend to
            directly edit values for any reason, do not forget to invalidate the
            cache: ``self.size=None``

        :return: :py:class:`ItemSize` DynamoDB item size in bytes
        """

        # Check cache and compute
        if self.size is None:
            size = 0

            for key in self.keys():
                size += self._internal_item_size('S', key)
                size += self.get_field_size(key)

            self.size = size

        return ItemSize(self.size)

    def __sub__(self, other):
        """
        Utility function to compute a 'diff' of 2 Items. All fields of ``self``
        (left operand) identical to those of ``other`` (right operand) are dicarded.
        The other fields from ``self`` are kept. This proves to be extremely
        useful to support ``ALL_NEW`` and ``ALL_OLD`` return specification of
        ``UpdateItem`` in a clean and readable manner.

        :param other: ``Item`` to be used as filter

        :return: dict with fields of ``self`` not in or different from ``other``
        """
        # Thanks mnoel :)
        return {k:v for k,v in self.iteritems() if k not in other or v != other[k]}
