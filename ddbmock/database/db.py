# -*- coding: utf-8 -*-

from .table import Table
from .item import ItemSize
from .storage import Store
from collections import defaultdict
from ddbmock import config
from ddbmock.utils import push_write_throughput, push_read_throughput, schedule_action
from ddbmock.errors import (ResourceNotFoundException,
                            ResourceInUseException,
                            LimitExceededException,
                           )

# All validations are performed on *incomming* data => already done :)

class DynamoDB(object):
    """
    Main database, behaves as a singleton in the sense that all instances share
    the same data.

    If underlying store supports it, all tables schema are persisted at creation
    time to a special table ``~*schema*~`` which is an invalid DynamoDB table name
    so no collisions are to be expected.
    """
    _shared_data = {
        'data': {},
        'store': None,
    }

    def __init__(self):
        """
        When first instanciated, ``__init__`` checks the underlying store for
        potentially persisted tables. If any, it reloads there schema to make
        them available to the application.

        In all other cases, ``__init__`` simply loads the shared state.
        """
        cls = type(self)
        self.__dict__ = cls._shared_data

        # At first instanciation, attempt to reload the database schema
        if self.store is None:
            self.store = Store('~*schema*~')
            for table in self.store:
                self.data[table.name] = table

    def hard_reset(self):
        """
        Reset and drop all tables. If any data was persisted, it will be completely
        lost after a call to this method. I do use in ``tearDown`` of all ddbmock
        tests to avaid any side effect.
        """
        for table in self.data.values():
            table.truncate()

        self.data.clear()
        self.store.truncate()

    def list_tables(self):
        """
        Get a list of all table names.
        """
        return self.data.keys()

    def get_table(self, name):
        """
        Get a handle to :py:class:`ddbmock.database.table.Table` '``name``' is it exists.

        :param name: Name of the table to load.

        :return: :py:class:`ddbmock.database.table.Table` with name '``name``'

        :raises: :py:exc:`ddbmock.errors.ResourceNotFoundException` if the table does not exist.
        """
        if name in self.data:
            return self.data[name]
        raise ResourceNotFoundException("Table {} does not exist".format(name))

    def create_table(self, name, data):
        """
        Create a :py:class:`ddbmock.database.table.Table` named '``name``'' using
        parameters provided in ``data`` if it does not yet exist.

        :param name: Valid table name. No further checks are performed.
        :param data: raw DynamoDB request data.

        :return: A reference to the newly created :py:class:`ddbmock.database.table.Table`

        :raises: :py:exc:`ddbmock.errors.ResourceInUseException` if the table already exists.
        :raises: :py:exc:`ddbmock.errors.LimitExceededException` if more than :py:const:`ddbmock.config.MAX_TABLES` already exist.
        """
        if name in self.data:
            raise ResourceInUseException("Table {} already exists".format(name))
        if len(self.data) >= config.MAX_TABLES:
            raise LimitExceededException("Table limit reached. You can not have more than {} tables simultaneously".format(config.MAX_TABLES))

        self.data[name] = Table.from_dict(data)
        self.store[name, False] = self.data[name]
        return self.data[name]

    def _internal_delete_table(self, table):
        """This is ran only after the timer is exhausted.
        Important note: this function is idempotent. If another table with the
        same name has been created in the mean time, it won't be overwrittem.
        This is the kind of special cases you might encounter in testing
        environenment"""
        name = table.name
        if name in self.data and self.data[name] is table:
            self.data[name].store.truncate()  # FIXME: should be moved in table
            del self.data[name]
            del self.store[name, False]

    def delete_table(self, name):
        """
        Triggers internal "realistic" table deletion. This implies changing
        the status to ``DELETING``. Once :py:const:ddbmock.config.DELAY_DELETING
        has expired :py:meth:_internal_delete_table is called and the table
        is de-referenced from :py:attr:data.

        Since :py:attr:data only holds a reference, the table object might still
        exist at that moment and possibly still handle pending requests. This also
        allows to safely return a handle to the table object.

        :param name: Valid table name.

        :return: A reference to :py:class:`ddbmock.database.table.Table` named ``name``
        """
        if name not in self.data:
            raise ResourceNotFoundException("Table {} does not exist".format(name))

        table = self.data[name]
        table.delete()
        schedule_action(config.DELAY_DELETING, self._internal_delete_table, [table])

        return table

    def get_batch(self, batch):
        """
        Batch processor. Dispatches call to appropriate :py:class:`ddbmock.database.table.Table`
        methods. This is the only low_level API that directly pushes throughput usage.

        :param batch: raw DynamoDB request batch.

        :returns: dict compatible with DynamoDB API

        :raises: :py:exc:`ddbmock.errors.ValidationException` if a ``range_key`` was provided while table has none.
        :raises: :py:exc:`ddbmock.errors.ResourceNotFoundException` if a table does not exist.
        """
        ret = defaultdict(dict)

        for tablename, batch in batch.iteritems():
            base_capacity = 1 if batch[u'ConsistentRead'] else 0.5
            fields = batch[u'AttributesToGet']
            table = self.get_table(tablename)
            units = ItemSize(0)
            items = []
            for key in batch[u'Keys']:
                item = table.get(key, fields)
                if item:
                    units += item.get_size().as_units()
                    items.append(item)
            push_read_throughput(tablename, base_capacity*units)
            ret[tablename][u'Items'] = items
            ret[tablename][u'ConsumedCapacityUnits'] = base_capacity*units

        return ret

    def write_batch(self, batch):
        """
        Batch processor. Dispatches call to appropriate :py:class:`ddbmock.database.table.Table`
        methods. This is the only low_level API that directly pushes throughput usage.

        :param batch: raw DynamoDB request batch.

        :returns: dict compatible with DynamoDB API

        :raises: :py:exc:`ddbmock.errors.ValidationException` if a ``range_key`` was provided while table has none.
        :raises: :py:exc:`ddbmock.errors.ResourceNotFoundException` if a table does not exist.
        """
        ret = defaultdict(dict)

        for tablename, operations in batch.iteritems():
            table = self.get_table(tablename)
            units = ItemSize(0)
            for operation in operations:
                if u'PutRequest' in operation:
                    old, new = table.put(operation[u'PutRequest'][u'Item'], {})
                    units += max(old.get_size().as_units(), new.get_size().as_units())
                if u'DeleteRequest' in operation:
                    old = table.delete_item(operation[u'DeleteRequest'][u'Key'], {})
                    units += old.get_size().as_units()
            push_write_throughput(tablename, units)
            ret[tablename][u'ConsumedCapacityUnits'] = units

        return ret

dynamodb = DynamoDB()
"""Reference :py:class:`DynamoDB` instance. You should use it directly"""
