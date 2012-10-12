# -*- coding: utf-8 -*-

from .table import Table
from collections import defaultdict
from ddbmock.errors import (ResourceNotFoundException,
                            ResourceInUseException,
                            LimitExceededException,
                           )

MAX_TABLES = 256

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
            raise ResourceInUseException("Table {} already exists".format(name))
        if len(self.data) >= MAX_TABLES:
            raise LimitExceededException("Table limit reached. You can have more than {} tables simultaneously".format(MAX_TABLES))

        self.data[name] = Table.from_dict(data)
        return self.data[name]

    def delete_table(self, name):
        if name not in self.data:
            raise ResourceNotFoundException("Table {} does not exist".format(name))
        self.data[name].delete()
        ret = self.data[name].to_dict(verbose=False) # Not really the best place either...
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
                if item:
                    units += 0.5  # STUB
                    items.append(item)
            ret[tablename][u'Items'] = items
            ret[tablename][u'ConsumedCapacityUnits'] = units

        return ret

    def write_batch(self, batch):
        ret = defaultdict(dict)

        for tablename, operations in batch.iteritems():
            table = self.get_table(tablename)
            units = 0
            for operation in operations:
                if u'PutRequest' in operation:
                    table.put(operation[u'PutRequest'][u'Item'], {})
                if u'DeleteRequest' in operation:
                    table.delete_item(operation[u'DeleteRequest'][u'Key'], {})
                units += 1  # STUB
            ret[tablename][u'ConsumedCapacityUnits'] = units

        return ret
