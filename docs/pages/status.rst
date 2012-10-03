##############
Current Status
##############

Methods support
===============

- ``CreateTable`` DONE
- ``DeleteTable`` DONE
- ``UpdateTable`` DONE
- ``DescribeTable`` DONE
- ``GetItem DONE
- ``PutItem`` DONE
- ``DeleteItem`` DONE
- ``UpdateItem`` ALMOST
- ``BatchGetItem`` WIP
- ``BatchWriteItem`` TODO
- ``Query`` WIP
- ``Scan`` WIP

There is basically no support for ``Limit``, ``ExclusiveStartKey``,
``ScanIndexForward`` and their associated features at all in ddbmock. This
affects all "WIP" functions.

``UpdateItem`` has a different behavior when the target item did not exist prior
the update operation. In particular, the ``ADD`` operator will always behave as
though the item existed before.

Comparison Operators
====================

Some comparison might not work as expected on binary data as it is performed on
the base64 representation instead of the binary one. Please report a bug if this
is a problem for you, or, even better, open a pull request :)

Common to ``Query`` and ``Scan``
--------------------------------

Specific to ``Scan``
--------------------


Rates and size limitations
==========================

basically, none are supported yet

Request rate
------------

- Throttle read  operations when provisioned throughput exceeded. TODO
- Throttle write operations when provisioned throughput exceeded. TODO
- Report accurate throughput. WONT FIX

ddbmock currently reports the consumed throughput based on item count. Their
size is ignored from the computation. While it is theoretically possible, it
would no be accurate anyway because we can not reproduce exactly Amazon's storage
efficiency.

Actually, this is even trickier as the throughput is normally spreaded among
partitions which ddbmock does not handle.

Request size
------------

- Limit response size to 1MB. TODO
- Limit request size to 1MB. TODO
- Limit ``BatchGetItem`` to 100 per request. TODO
- Linit ``BatchWriteItem`` to 25 per request. TODO

Table managment
---------------

- No more than 10 ``CREATING`` tables. TODO
- No more than 10 ``DELETING`` tables. TODO
- No more than 1  ``UPDATING`` table.  TODO

- No more than 1 Throughput decrease/day. DONE
- No more than *2 Throughput increase/day. DONE
