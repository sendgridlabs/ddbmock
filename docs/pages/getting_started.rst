##################################
Getting started with DynamoDB-mock
##################################

.. include:: ../_include/intro.rst

Installation
============

::

    $ pip install ddbmock


Example usage
=============

Run as Regular client-server
----------------------------

Ideal for test environment. For stage and production I highly recommend using
DynamoDB servers. ddbmock comes with no warranty and *will* **loose your data(tm)**.

::

    $ pserve development.ini # launch the server on 0.0.0.0:6543

::

    import boto
    from ddbmock import connect_ddbmock

    # Use the provided helper to connect your *own* endpoint
    db = connect_ddbmock()

    # Done ! just use it wherever in your project as usual.
    db.list_tables() # get list of tables (empty at this stage)

Note: if you do not want to import ddbmock only for the helper, here is a
reference implementation:

::

    def connect_ddbmock(host='localhost', port=6543):
        import boto
        from boto.regioninfo import RegionInfo
        endpoint = '{}:{}'.format(host, port)
        region = RegionInfo(name='ddbmock', endpoint=endpoint)
        return boto.connect_dynamodb(region=region, port=port, is_secure=False)

Run as a standalone library
---------------------------

Ideal for unit testing or small scale automated functional tests. Nice to play
around with boto DynamoDB API too :)

::

    import boto
    from ddbmock import connect_boto

    # Wire-up boto and ddbmock together
    db = connect_boto()

    # Done ! just use it wherever in your project as usual.
    db.list_tables() # get list of tables (empty at this stage)
