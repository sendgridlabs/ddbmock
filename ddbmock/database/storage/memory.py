# -*- coding: utf-8 -*-

from collections import defaultdict

class Store(object):
    def __init__(self, name):
        """
        Initialize the in-memory store

        :param name: Table name.
        """
        self.name = name
        self.data = defaultdict(dict)

    def truncate(self):
        """Perform a full table cleanup. Might be a good idea in tests :)"""
        self.data = defaultdict(dict)

    def __getitem__(self, keys):
        """
        Get item at ``keys``.

        :param key: ``keys`` List
        :return: Item or item dict

        :raise: KeyError
        """

        keys = tuple(keys)
        if keys not in self.data:
            raise KeyError('keys={} not found'.format(keys))
        return self.data[keys]

    def __setitem__(self, keys, item):
        """
        Set the item at ``keys``.

        :param key: (``hash_key``, ``range_key``) Tuple.
        :param item: the actual ``Item`` data structure to store
        """

        keys = tuple(keys)
        self.data[keys] = item

    def __delitem__(self, keys):
        """
        Delete item at key ``keys``

        :raises: KeyError if not found
        """

        keys = tuple(keys)
        # Let this line throw KeyError if needed. Checks needs to be performed by the caller
        del self.data[keys]

    def __iter__(self):
        """
        Iterate all over the table, abstracting the ``hash_key`` and
        ``range_key`` complexity. Mostly used for ``Scan`` implementation.
        """

        for outer in self.data.values():
            for item in outer.values():
                yield item
