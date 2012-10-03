ddbmock -- a DynamoDB mock implementation.

Presentation
============

`DynamoDB <http://aws.amazon.com/dynamodb/>`_ is a minimalistic NoSQL engine
provided by Amazon as a part of their AWS product.

**DynamoDB** allows you to store documents composed of unicode, number or binary
data as well are sets. Each tables must define a ``hash_key`` and may define a
``range_key``. All other fields are optional.

**DynamoDB** is really awesome but is terribly slooooow with managment tasks.
This makes it completly unusable in test environements

**ddbmock** brings a nice, tiny, in-memory implementation of DynamoDB along with
much better and detailed error messages. Among its niceties, it features a double
entry point:

 - regular network based entry-point with 1:1 correspondance with stock DynamoDB
 - **embeded entry-point** with seamless boto intergration 1, ideal to avoid spinning yet another server.

Current status
==============

ddbmock is an experimental project and is currently under heavy development. It
also may be discontinued at *any* time.

- support full table life-cycle
- support full item life-cycle
- preliminary support of ``Query``, ``Scan`` and ``BatchGetItem``
- support (almost) all types restrictions
- no limits on table number nor concurent table operations
- no limits on item size
- no limits for request/response size nor item count in those

See CHANGELOG for up-to-date status.

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


Requirements
============

 - Python 2.7.x
 - Pyramid >= 1.3
 - Boto >= 2.5.0 (optional)
 - **NO** AWS account :)

Related Links
=============

ddbmock
-------

- **Full documentation**: TBD
- **Report bugs**: https://bitbucket.org/Ludia/dynamodb-mock/issues
- **Download**: http://pypi.python.org/pypi/ddbmock

Dynamodb-mapper
---------------

- **Full documentation**: http://dynamodb-mapper.readthedocs.org/en/latest/
- **Report bugs**: https://bitbucket.org/Ludia/dynamodb-mapper/issues
- **Download**: http://pypi.python.org/pypi/dynamodb-mapper

Boto
----

- **Full documentation**: http://docs.pythonboto.org/en/latest/index.html
- **Report bugs**: https://github.com/boto/boto/issues
- **Download**: http://pypi.python.org/pypi/boto
