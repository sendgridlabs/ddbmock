# -*- coding: utf-8 -*-

from ddbmock.errors import ConditionalCheckFailedException

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
            typename, value = self[name].iteritems().next()
        except KeyError:
            raise ValueError('Field {} not found'.format(key.name))

        if key.typename != typename:
            raise TypeError('Expected key type = {} for field {}. Got {}'.format(
                key.typename, key.name, typename))

        return value