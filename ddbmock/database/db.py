# -*- coding: utf-8 -*-

from .table import Table

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
        return None

    def create_table(self, name, data):
        if name in self.data:
            return None
        self.data[name] = Table.from_dict(data)
        return self.data[name]

    def delete_table(self, name):
        if name not in self.data:
            return None
        self.data[name].delete()
        ret = self.data[name].to_dict()
        del self.data[name]
        return ret