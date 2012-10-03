##############
Current Status
##############

This documents reflects ddbmock status as of 3/10/12. It may be outdated.

Methods support
===============

- ``CreateTable`` DONE
- ``DeleteTable`` DONE
- ``UpdateTable`` DONE
- ``DescribeTable`` DONE
- ``GetItem`` DONE
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

All operators exists as lower case functions in ``ddbmock.database.comparison``.
This list can easily be extended to add new/custom operators.

Common to ``Query`` and ``Scan``
--------------------------------

- ``EQ`` DONE
- ``LE`` DONE
- ``LT`` DONE
- ``GE`` DONE
- ``GT`` DONE
- ``BEGINS_WITH`` DONE
- ``BETWEEN`` DONE

Specific to ``Scan``
--------------------

- ``NULL`` DONE
- ``NOT_NULL`` DONE
- ``CONTAINS`` DONE
- ``NOT_CONTAINS`` DONE
- ``IN`` DONE

``IN`` operator is the only that can not be imported directly as it overlaps
builtin ``in`` keyword. If you need it, either import it with ``getattr`` on the
module or as ``in_test`` which, anyway, is its internal name.

Rates and size limitations
==========================

basically, none are supported yet

Request rate
------------

- Throttle read  operations when provisioned throughput exceeded. TODO
- Throttle write operations when provisioned throughput exceeded. TODO
- Maximum throughput is 10,000. DONE
- Minimum throughput is 1. DONE
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

- No more than 255 tables. TODO
- No more than 10 ``CREATING`` tables. TODO
- No more than 10 ``DELETING`` tables. TODO
- No more than 1  ``UPDATING`` table.  TODO

- No more than 1 Throughput decrease/calendar day. BUGGY (24h instead of calendar day)
- No more than *2 Throughput increase/update. DONE
- At least 10% change per update. TODO

Types and items Limitations
===========================

- Table names can only be between 3 and 255 bytes long. DONE
- Table names can only contains a-z, A-Z, 0-9, '_', '-', and '.'. DONE
- No more than 64kB/Item including fieldname and indexing overhead. TODO
- Primary key names can only be between 1 and 255 bytes long. DONE
- Attribute value can *not* be Null. DONE
- ``hash_key`` value smaller than 2048 bytes. TODO
- ``range_key`` value smaller than 1024 bytes. TODO
- Numbers can have up to 38 digits precision and can be between 10^-128 to 10^+126. PARTIAL
