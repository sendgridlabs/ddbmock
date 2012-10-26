=================
ddbmock 0.4.0.dev
=================

This section documents all user visible changes included between ddbmock
versions 0.3.2 and versions 0.4.0

This iteration is focused on making code leaner with better documentation.

Additions
---------

- consistent_read parameter to ``Query``
- central config.py file with all constraints
- timer for table status changes
- full ``Query`` support

Removal
-------

- legacy ``connect_boto`` and ``connect_ddbmock``
- ``dynamodb_api_validate`` decorator. It is now called automatically
- ``wrap_exceptions`` decorator. It is now integrated to the router

Changes
-------

- Move from Voluptuous to Onctuous for validations, less code
- fix server startup with pserver (bad backage name)
- fix server crash on validation exception (bad serialization)
- accurate throughput for all Read  operations
- accurate throughput for all Write operations
- move 'views' to 'routes'
- remove all pyramid code from 'views'/'routes'
- pyramid and boto entry points now shares most of the router
- pre-instanciate DynamoDB as dynamodb

Upgrade
-------

- rename ``connect_boto`` to ``connect_boto_patch``
- rename ``connect_ddbmock`` to ``connect_boto_network``
- rename all ``DynamoDB() to ``dynamodb``
- replace ...import DynamoDB by ... import dynamodb


=============
ddbmock 0.3.2
=============

This section documents all user visible changes included between ddbmock
versions 0.3.1 and versions 0.3.2

This iteration was focused on passing boto integration tests.

Additions
---------

- preliminary batchWriteItem support

Changes
-------

- fix number validation
- fix: item where created by defaultdict magic when looking for bogus item.
- return no Item field when not found, but empty when filtered
- [botopatch] handle DynamoDBConditionalCheckFailedError error

=============
ddbmock 0.3.1
=============

This section documents all user visible changes included between ddbmock
versions 0.3.0 and versions 0.3.1

This iteration was focused on accuracy

Additions
---------

- 100% tests coverage
- add basic tests for pyramid entry-point (#1)
- add plenty of unit and functional tests. Coverage is 100%
- add support for all ``ALL_OLD`` ``ALL_NEW`` ``UPDATED_OLD`` ``UPDATED_NEW`` in ``UpdateItem``
- add accurate field size calculation
- add accurate item size calculation
- add accurate table size calculation
- add MAX_TABLES check at table creation

Changes
-------

- accurate table statuses
- fix pyramid entry-point
- fix list validations. Len limitation was not working
- attempt to store empty field/set raise ValidationError (#4)
- accurate exception detection and reporting in UpdateTable
- accurate ``hash_key`` and ``range_key`` size validation
- accurate number limitations (max 38 digits precision; between 10^-128 and 10^+126)
- rename ``connect_boto`` to ``connect_boto_patch`` + compat layer
- rename ``connect_ddbmock`` to ``connect_boto_network`` + compat layer
- block PutItem/UpdateItem when bigger than ``MAX_ITEM_SIZE``

Upgrade
-------

Nothing mandatory as this is a minor release but, I recommend that you:

- rename ``connect_boto`` to ``connect_boto_patch``
- rename ``connect_ddbmock`` to ``connect_boto_network``

=============
ddbmock 0.3.0
=============

Initial ddbmock release. This is *alpha quality* sofware. Some
import features such as "Excusive Start Key", "Reverse" and
"Limit" as well as ``BatchWriteItem`` have not been written (yet).

Additions
---------

- entry-point WEB  (network mode)
- entry-point Boto (standalone mode)
- support for ``CreateTable`` method
- support for ``DeleteTable`` method
- support for ``UpdateTable`` method
- support for ``DescribeTable`` method
- support for ``GetItem method
- support for ``PutItem`` method
- support for ``DeleteItem`` method
- support for ``UpdateItem`` method (small approximations)
- support for ``BatchGetItem`` method (initial)
- support for ``Query`` method (initial)
- support for ``Scan`` method (initial)
- all comparison operators
- aggresive input validation

Known bugs - limitations
------------------------

- no support for ``BatchWriteItem``
- no support for "Excusive Start Key", "Reverse" and "Limit" in
``Query`` and ``Scan``
- no support for "UnprocessedKeys" in ``BatchGetItem``
- Web entry-point is untested, fill bugs if necessary :)
