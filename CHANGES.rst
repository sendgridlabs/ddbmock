=============
ddbmock 0.3.1
=============

This section documents all user visible changes included between ddbmock
versions 0.3.0 and versions 0.3.1.dev

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
