# -*- coding: utf-8 -*-

# All validations are performed on *incomming* data => already done :)

class Key(object):
    def __init__(self, name, typename):
        self.name = name
        self.typename = typename

    def read(self, key):
        typename, value = key.items()[0]
        if self.typename != typename:
            raise TypeError('Expected key type = {} for field {}. Got {}'.format(
                self.typename, self.name, typename))

        return value

    def to_dict(self):
        return {
            "AttributeName": self.name,
            "AttributeType": self.typename,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data[u'AttributeName'], data[u'AttributeType'])

class PrimaryKey(Key):
    pass