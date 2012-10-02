# -*- coding: utf-8 -*-

from .table import Table
from collections import defaultdict
from ddbmock.errors import ResourceNotFoundException

# All validations are performed on *incomming* data => already done :)

class DynamoDB(object):
    shared_data = {
        'data': {}
    }

    def __init__(self):
        cls = type(self)
        self.__dict__ = cls.shared_data

    def hard_reset(self):
        self.data.clear()

    def list_tables(self):
        return self.data.keys()

    def get_table(self, name):
        if name in self.data:
            return self.data[name]
        raise ResourceNotFoundException("Table {} does not exist".format(name))

    def create_table(self, name, data):
        if name in self.data:
            return None
        self.data[name] = Table.from_dict(data)
        return self.data[name]

    def delete_table(self, name):
        if name not in self.data:
            raise ResourceNotFoundException("Table {} does not exist".format(name))
        self.data[name].delete()
        ret = self.data[name].to_dict()
        del self.data[name]
        return ret

    def get_batch(self, batch):
        ret = defaultdict(dict)

        for tablename, keys in batch.iteritems():
            fields = keys[u'AttributesToGet'] if u'AttributesToGet' in keys else []
            table = self.get_table(tablename)
            units = 0
            items = []
            for key in keys[u'Keys']:
                item = table.get(key, fields)
                units += 0.5  # STUB
                if item: items.append(item)
            ret[tablename][u'Items'] = items
            ret[tablename][u'ConsumedCapacityUnits'] = len(items)*0.5

        return ret