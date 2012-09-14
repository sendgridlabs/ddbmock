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

class PrimaryKey(Key):
    valid_types = ['N', 'S', 'B']

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

class DynamoDB(object):
    shared_data = {}

    def __init__(self):
        cls = type(self)
        self.__dict__['data'] = cls.shared_data

    def list_tables(self):
        return self.data.keys()

    def get_table(self, name):
        if name in self.data:
            return self.data[name]
        return None

    def create_table(self, name, *k):
        if name in self.data:
            return None
        self.data[name] = Table(name, *k)
        return self.data[name]

    def delete_table(self, name):
        if name not in self.data:
            return None
        self.data[name].delete()
        ret = self.data[name].to_dict()
        del self.data[name]
        return ret