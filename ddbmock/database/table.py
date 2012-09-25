# -*- coding: utf-8 -*-

from .key import Key, PrimaryKey
from .item import Item
from collections import defaultdict
from ddbmock.errors import ValidationException

# All validations are performed on *incomming* data => already done :)

class Table(object):
    def __init__(self, name, rt, wt, hash_key, range_key):
        self.name = name
        self.rt = rt
        self.wt = wt
        self.hash_key = hash_key
        self.range_key = range_key
        self.status = "ACTIVE"
        self.data = defaultdict(lambda: defaultdict(Item))

    def delete(self):
        #stub
        self.status = "DELETING"

    def update_throughput(self, rt, wt):
        # TODO: check update rate
        self.rt = rt
        self.wt = wt

    def put(self, item, expected):
        item = Item(item)
        try:
            hash = item.read_key(self.hash_key)
            range = item.read_key(self.range_key)
        except KeyError:
            raise ValidationException("Either hash, range or both key is missing")

        old = self.data[hash][range]
        old.assert_match_expected(expected)

        self.data[hash][range] = item

        return old

    def get(self, key, fields):
        key = Item(key)
        try:
            hash = key.read_key(self.hash_key, u'HashKeyElement')
            range = key.read_key(self.range_key, u'RangeKeyElement')
        except KeyError:
            raise ValidationException("Either hash, range or both key is missing")

        item = self.data[hash][range]

        return item.filter(fields)

    @classmethod
    def from_dict(cls, data):
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