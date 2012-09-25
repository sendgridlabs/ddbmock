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