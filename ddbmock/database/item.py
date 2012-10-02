# -*- coding: utf-8 -*-

from ddbmock.errors import ConditionalCheckFailedException
from decimal import Decimal
from . import comparison

class Item(dict):
    def filter(self, fields):
        """
        Return a dict containing only the keys specified in ``fields``. If
        ``fields`` evaluates to False (None, empty, ...), the original dict is
        returned untouched.

        :ivar fields: array of name of keys to keep
        :return: filtered ``item``
        """
        if fields:
            return dict((k, v) for k, v in self.items() if k in fields)
        return dict(self)

    def is_new(self):
        return not len(self)

    def _apply_action(self, fieldname, action):
        # Rewrite this function, it's disgutting code
        #FIXME: temp hack
        if u"Action" not in action:
            action[u'Action'] = u"PUT"

        if action[u'Action'] == u"PUT":
            self[fieldname] = action[u'Value']
        if action[u'Action'] == u"DELETE": # Starts to be anoying
            if not fieldname in self:
                return  #shortcut
            if u'Value' not in action:
                del self[fieldname] # Nice and easy part
                return

            typename, value = action[u'Value'].items()[0]
            ftypename, fvalue = self[fieldname].items()[0]

            if len(ftypename) != 2:
                raise TypeError("Can not DELETE elements from a non set type. Got {}".format(ftypename))
            if ftypename != typename:
                raise TypeError("Expected type {t} for DELETE from type {t}. Got {}".format(typename, t=ftypename))

            # do the dirty work
            data = set(fvalue).difference(value)
            # if data empty => remove the key
            if not data:
                del self[fieldname]
            else:
                self[fieldname] = {ftypename: list(data)}

        if action[u'Action'] == u"ADD":  # Realy anoting to code :s
            #FIXME: not perfect, action should be different if the item was new
            typename, value = action[u'Value'].items()[0]
            if fieldname in self:
                ftypename, fvalue = self[fieldname].items()[0]

                if ftypename == u"N":
                    data = Decimal(value) + Decimal(fvalue)
                    self[fieldname][u"N"] = unicode(data)
                elif ftypename in [u"NS", u"SS", u"BS"]:
                    if ftypename != typename:
                        raise TypeError("Expected type {t} for ADD in type {t}. Got {}".format(typename, t=ftypename))
                    data = set(fvalue).union(value)
                    self[fieldname][typename] = list(data)
                else:
                    TypeError("Only N, NS, SS and BS types supports ADD operation. Got {}".format(ftypename))
            else:
                if typename not in [u"N", u"NS"]:
                    raise ValueError("When performing ADD operation on new field, only Numbers or Numbers set are allowed. Got {} of type {}".format(value, typename))
                self[fieldname] = action[u'Value']

    def apply_actions(self, actions):
        map(self._apply_action, actions.keys(), actions.values())

    def assert_match_expected(self, expected):
        """
        Raise ConditionalCheckFailedException if ``self`` does not match ``expected``
        values. ``expected`` schema is raw conditions as defined by DynamoDb.

        :ivar expected: conditions to validate
        :raises: ConditionalCheckFailedException
        """
        for fieldname, condition in expected.iteritems():
            if u'Exists' in condition and not condition[u'Exists']:
                if fieldname in self:
                    raise ConditionalCheckFailedException(
                        "Field '{}' should not exist".format(fieldname))
                continue
            if fieldname not in self:
                raise ConditionalCheckFailedException(
                    "Field '{}' should exist".format(fieldname))
            if self[fieldname] != condition[u'Value']:
                raise ConditionalCheckFailedException(
                    "Expected field '{}'' = '{}'. Got '{}'".format(
                    fieldname, condition[u'Value'], self[fieldname]))

    def match(self, conditions):
        for name, condition in conditions.iteritems():
            if not self.field_match(name, condition):
                return False

        return True

    def field_match(self, name, condition):
        """Check if a field matches a condition. Return False when field not
        found, or do not match. If condition is None, it is considered to match.

        :ivar name: name of the field to test
        :ivar condition: raw dict describing the condition {"OPERATOR": FIELDDEFINITION}
        :return: True on success
        """
        # Arcording to specif, no condition means match
        if condition is None:
            return True

        # read the item
        if name not in self:
            value = None
        else:
            value = self[name]

        # Load the test operator from the comparison module. Thamks to input
        # validation, no try/except required
        condition_operator = condition[u'ComparisonOperator'].lower()
        operator = getattr(comparison, condition_operator)
        return operator(value, *condition[u'AttributeValueList'])

    def read_key(self, key, name=None):
        """Provided ``key``, read field value at ``name`` or ``key.name`` if not
        specified. If the field does not exist, this is a "ValueError". In case
        it exists, also check the type compatibility. If it does not match, raise
        TypeError.

        :ivar key: ``Key`` or ``PrimaryKey`` to read
        :ivar name: override name field of key
        :return: field value
        """
        if key is None:
            return False
        if name is None:
            name = key.name

        try:
            field = self[name]
        except KeyError:
            raise ValueError('Field {} not found'.format(name))

        return key.read(field)