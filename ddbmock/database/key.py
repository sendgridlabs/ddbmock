# -*- coding: utf-8 -*-

import re

class Key(object):
    valid_types = ['N', 'S', 'B', 'NS', 'SS']
    min_len = 1
    max_len = 255

    def validate(self, name, typename):
        cls = type(self)
        if typename not in cls.valid_types:
            raise TypeError("Type must be one of {}. Got {}".format(cls.valid_types, typename))
        l = len(name)
        if (l < cls.min_len) or (l > cls.max_len):
            raise TypeError("Name len must be between {} and {}. Got {}".format(cls.min_len, cls.max_len, l))

    def __init__(self, name, typename):
        self.validate(name, typename)
        self.name = name
        self.typename = typename

    def to_dict(self):
        return {
            "AttributeName": self.name,
            "AttributeType": self.typename,
        }

    @classmethod
    def from_dict(cls, data):
        if u'AttributeName' not in data:
            raise TypeError("No attribute name")
        if u'AttributeType' not in data:
            raise TypeError("No attribute type")

        return cls(data[u'AttributeName'], data[u'AttributeType'])

class PrimaryKey(Key):
    valid_types = ['N', 'S', 'B']