# -*- coding: utf-8 -*-

from .key import Key, PrimaryKey
from .item import Item
from sys import getsizeof
from collections import defaultdict
from ddbmock.errors import ValidationException
import time

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
        self.creation_time = time.time()
        self.last_increase_time = 0
        self.last_decrease_time = 0
        self.count = 0

    def delete(self):
        #stub
        self.status = "DELETING"

    def update_throughput(self, rt, wt):
        # is decrease ?
        if self.rt > rt or self.wt > wt:
            current_time = time.time()
            if current_time - self.last_decrease_time < 24*60*60:
                return # Brrr, silent ignore. Should raise something but what ?
            self.last_decrease_time = current_time

        # is increase ?
        if self.rt < rt or self.wt < wt:
            if self.rt * 2 < rt or self.wt * 2 < wt:
                return # Brrr, silent ignore. Should raise something but what ?
            self.last_increase_time = time.time()

        self.rt = rt
        self.wt = wt

    def delete_item(self, key, expected):
        key = Item(key)
        try:
            hash = key.read_key(self.hash_key, u'HashKeyElement')
            range = key.read_key(self.range_key, u'RangeKeyElement')
        except KeyError:
            raise ValidationException("Either hash, range or both key is missing")

        old = self.data[hash][range]
        old.assert_match_expected(expected)

        if self.range_key is None:
            del self.data[hash]
        else:
            del self.data[hash][range]

        return old

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

        # If this a new item, increment counter
        if not old:
            self.count += 1

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
        """Serialize table metadata for the describe table method. ItemCount and
        TableSizeBytes are accurate but highly depends on CPython > 2.6. Do not
        rely on it to project the actual size on a real DynamoDB implementation.
        """
        ret = {
            "CreationDateTime": self.creation_time,
            "ItemCount": self.count,
            "KeySchema": {
                "HashKeyElement": self.hash_key.to_dict(),
            },
            "ProvisionedThroughput": {
                "ReadCapacityUnits": self.rt,
                "WriteCapacityUnits": self.wt,
            },
            "TableName": self.name,
            "TableSizeBytes": getsizeof(self.data),
            "TableStatus": self.status
        }

        if self.last_increase_time:
            ret[u'ProvisionedThroughput'][u'LastIncreaseDateTime'] = self.last_increase_time
        if self.last_decrease_time:
            ret[u'ProvisionedThroughput'][u'LastDecreaseDateTime'] = self.last_decrease_time

        if self.range_key is not None:
            ret[u'KeySchema'][u'RangeKeyElement'] = self.range_key.to_dict()

        return ret