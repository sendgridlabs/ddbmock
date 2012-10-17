#######################
Extending DynamoDB-mock
#######################

Folder structure
================

::

    DynamoDB-Mock
    +-- ddbmock
    |   +-- database   => the storage enginr
    |   +-- router     => entry-points logic
    |   +-- routes     => each DynamoDB method has a file here
    |   `-- validators => request syntax validation middleware
    +-- docs
    |   `-- pages
    `-- tests
        +-- unit        => mainly details and corner cases tests
        `-- functional
            +-- boto    => main/extensive tests
            `-- pyramid => just make sure that all methods are supported


Adding a custom method
======================

Minimum version
---------------

As long as the method follows DynamoDB request structure, it is mostly a matter of
adding a file to ``ddbmock/routes`` with the following conventions:

 - file_name: "underscore" version of the camel case method name.
 - function_name: file_name.
 - argument: parsed post payload.
 - return: response dict.

Example: adding a ``HelloWorld`` method:

::

    # -*- coding: utf-8 -*-
    # module: ddbmock.routes.hello_world.py

    def hello_world(post):
        return {
            'Hello': 'World'
        }
