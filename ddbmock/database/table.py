# -*- coding: utf-8 -*-

import re

from .key import Key, PrimaryKey

class Table(object):
    mask = re.compile(r'^[a-zA-Z0-9\-_\.]*$')
    min_len = 3
    max_len = 255

    def __init__(self, name, rt, wt, hash_key, range_key):
        self.name = self._validate_name(name)
        self.rt = self._validate_throughput_value(rt)
        self.wt = self._validate_throughput_value(wt)
        self.hash_key = hash_key
        self.range_key = range_key
        self.status = "ACTIVE"

    def _validate_name(self, name):
        cls = type(self)
        l = len(name)
        if (l < cls.min_len) or (l > cls.max_len):
            raise TypeError("TableName len must be between {} and {}. Got {}".format(cls.min_len, cls.max_len, l))
        if cls.mask.match(name) is None:
            raise TypeError("TableName chars must match pattern {}. Got {}".format(cls.mask.pattern, name))
        return name

    def _validate_throughput_value(self, value):
        if value < 1 or value > 10000:
            raise ValueError("Throughput value must be between {} and {}. Got {}".format(1, 10000, value))
        return value

    def delete(self):
        #stub
        self.status = "DELETING"

    def update_throughput(self, rt, wt):
        # TODO: check update rate
        self.rt = self._validate_throughput_value(rt)
        self.wt = self._validate_throughput_value(wt)

    @classmethod
    def from_dict(cls, data):
        if u'TableName' not in data:
            raise TypeError("No table name supplied")
        if u'ProvisionedThroughput' not in data:
            raise TypeError("No throughput provisioned")
        if u'KeySchema' not in data:
            raise TypeError("No schema")
        if u'WriteCapacityUnits' not in data[u'ProvisionedThroughput']:
            raise TypeError("No WRITE throughput provisioned")
        if u'ReadCapacityUnits' not in data[u'ProvisionedThroughput']:
            raise TypeError("No READ throughput provisioned")

        if u'HashKeyElement' not in data[u'KeySchema']:
            raise TypeError("No hash_key")
        hash_key = PrimaryKey.from_dict(data[u'KeySchema'][u'HashKeyElement'])
        range_key = None
        if u'RangeKeyElement' in data[u'KeySchema']:
            range_key = PrimaryKey.from_dict(data[u'KeySchema'][u'RangeKeyElement'])

        return cls( data[u'TableName'],
                    data[u'ProvisionedThroughput'][u'ReadCapacityUnits'],
                    data[u'ProvisionedThroughput'][u'WriteCapacityUnits'],
                    hash_key,
                    range_key,
                  )

    def to_dict(self):
        ret = {
            "CreationDateTime":1.309988345372E9, #stub
            "ItemCount": 0, # Stub
            "KeySchema": {
                "HashKeyElement": self.hash_key.to_dict(),
            },
            "ProvisionedThroughput": {
                "LastIncreaseDateTime": 1.309988345384E9, #stub
                "ReadCapacityUnits": self.rt,
                "WriteCapacityUnits": self.wt,
            },
            "TableName": self.name,
            "TableSizeBytes": -1, #STUB
            "TableStatus": self.status
        }

        if self.range_key is not None:
            ret[u'KeySchema'][u'RangeKeyElement'] = self.range_key.to_dict()

        return ret