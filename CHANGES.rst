=================
ddbmock 0.3.1.dev
=================

This section documents all user visible changes included between ddbmock
versions 0.3.0 and versions 0.3.1.dev

Additions
---------

- add basic tests for pyramid entry-point (#1)

Changes
-------

- accurate table statuses
- fix pyramid entry-point

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
