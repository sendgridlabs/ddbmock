# -*- coding: utf-8 -*-

from .key import Key, PrimaryKey
from .item import Item
from sys import getsizeof
from collections import defaultdict
from ddbmock.errors import ValidationException
import time, copy

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
        hash_key = key.read_key(self.hash_key, u'HashKeyElement')
        range_key = key.read_key(self.range_key, u'RangeKeyElement')

        old = self.data[hash_key][range_key]
        old.assert_match_expected(expected)

        if self.range_key is None:
            del self.data[hash_key]
        else:
            del self.data[hash_key][range_key]

        if not old.is_new():
            # If this NOT new item, decrement counter
            self.count -= 1

        return old

    def update_item(self, key, actions, expected):
        key = Item(key)
        hash_key = key.read_key(self.hash_key, u'HashKeyElement')
        range_key = key.read_key(self.range_key, u'RangeKeyElement')

        # Need a deep copy as we will *modify* it
        old = copy.deepcopy(self.data[hash_key][range_key])
        old.assert_match_expected(expected)

        # Make sure we are not altering a key
        if self.hash_key.name in actions:
            raise ValidationException("UpdateItem can not alter the hash_key.")
        if self.range_key is not None and self.range_key.name in actions:
            raise ValidationException("UpdateItem can not alter the range_key.")

        self.data[hash_key][range_key].apply_actions(actions)

        # If new item:
        if old.is_new():
            # increment counter
            self.count += 1
            # append the keys, this is a new item
            self.data[hash_key][range_key][self.hash_key.name] = hash_key
            if self.range_key is not None:
                self.data[hash_key][range_key][self.range_key.name] = range_key

        return old

    def put(self, item, expected):
        item = Item(item)
        hash_key = item.read_key(self.hash_key)
        range_key = item.read_key(self.range_key)

        old = self.data[hash_key][range_key]
        old.assert_match_expected(expected)

        self.data[hash_key][range_key] = item

        # If this a new item, increment counter
        if not old:
            self.count += 1

        return old

    def get(self, key, fields):
        key = Item(key)
        hash_key = key.read_key(self.hash_key, u'HashKeyElement')
        range_key = key.read_key(self.range_key, u'RangeKeyElement')

        if self.range_key is None and u'RangeKeyElement' in key:
            raise ValidationException("Table {} has no range_key".format(self.name))

        item = self.data[hash_key][range_key]

        return item.filter(fields)

    def query(self, hash_key, rk_condition, fields, start, reverse, limit):
        """Scans all items at hash_key and return matches as well as last
        evaluated key if more than 1MB was scanned.

        :ivar hash_key: Element describing the hash_key, no type checkeing performed
        :ivar rk_condition: Condition which must be matched by the range_key. If None, all is returned.
        :ivar fields: return only these fields is applicable
        :ivar start: key structure. where to start iteration
        :ivar reverse: wether to scan the collection backward
        :ivar limit: max number of items to parse in this batch
        :return: results, last_key
        """
        #FIXME: naive implementation
        #TODO:
        # - reverse
        # - esk
        # - limit
        # - size limit
        # - last evaluated key

        hk_name = self.hash_key.read(hash_key)
        rk_name = self.range_key.name
        results = []

        for item in self.data[hk_name].values():
            if item.field_match(rk_name, rk_condition):
                results.append(item.filter(fields))

        return results, None

    def scan(self, scan_conditions, fields, start, limit):
        """Scans a whole table, no matter the structure, and return matches as
        well as the the last_evaluated key if applicable and the actually scanned
        item count.

        :ivar scan_conditions: Dict of key:conditions to match items against. If None, all is returned.
        :ivar fields: return only these fields is applicable
        :ivar start: key structure. where to start iteration
        :ivar limit: max number of items to parse in this batch
        :return: results, last_key, scanned_count
        """
        #FIXME: naive implementation (too)
        #TODO:
        # - reverse
        # - esk
        # - limit
        # - size limit
        # - last evaluated key

        scanned_count = 0
        results = []

        for outer in self.data.values():
            for item in outer.values():
                scanned_count += 1
                if item.match(scan_conditions):
                    results.append(item.filter(fields))

        return results, None, scanned_count


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