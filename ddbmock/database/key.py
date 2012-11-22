# -*- coding: utf-8 -*-

# All validations are performed on *incomming* data => already done :)

from ddbmock.errors import ValidationException

class Key(object):
    """
    Abstraction layer over DynamoDB Keys in :py:class:`ddbmock.database.item.Item`
    """
    def __init__(self, name, typename):
        """
        High level Python constructor

        :param name: Valid key name. No further checks are performed.
        :param typename: Valid key typename. No further checks are performed.
        """
        self.name = name
        self.typename = typename

    def read(self, key):
        """
        Parse a key as specified by DynamoDB API and return its value as long as
        its typename matches :py:attr:`typename`

        :param key: Raw DynamoDB request key.

        :return: the value of the key

        :raises: :py:exc:`ddbmock.errors.ValidationException` if field types does not match

        """
        typename, value = key.items()[0]
        if self.typename != typename:
            raise ValidationException('Expected key type = {} for field {}. Got {}'.format(
                self.typename, self.name, typename))

        return value

    def to_dict(self):
        """
        Return the key as a Python dict.

        :return: Serialized version of the key definition metadata compatible with DynamoDB API syntax.
        """
        return {
            "AttributeName": self.name,
            "AttributeType": self.typename,
        }

    @classmethod
    def from_dict(cls, data):
        """
        Alternate constructor which deciphers raw DynamoDB request data before
        ultimately calling regular ``__init__`` method.

        See :py:meth:`__init__` for more insight.

        :param data: raw DynamoDB request data.

        :return: fully initialized :py:class:`Key` instance
        """
        return cls(data[u'AttributeName'], data[u'AttributeType'])

class PrimaryKey(Key):
    """Special marker to provide distinction between regulat Keys and PrimaryKey"""
    pass
