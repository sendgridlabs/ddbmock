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

If the ``post`` of your method contains ``TableName``, you may auto-load the
corresponding table this way:

::

    # -*- coding: utf-8 -*-
    # module: ddbmock.routes.hello_world.py

    from ddbmock.utils import load_table()

    @load_table
    def hello_world(post):
        return {
            'Hello': 'World'
        }

Adding a custom validator
=========================

Let's say you want to let your new ``HelloWorld`` greet someone in particular,
you will want to add an argument to the request.

Example: simplest way to add support for an argument:

::

    # -*- coding: utf-8 -*-
    # module: ddbmock.routes.hello_world.py

    def hello_world(post):
        return {
            'Hello': 'World (and "{you}" too!)'.format(you=post['Name']
        }

Wanna test it?

>>> curl -d '{"Name": "chuck"}' -H 'x-amz-target: DynamoDB_custom.HelloWorld' localhost:6543
{'Hello': 'World (and "chuck" too!)'}

But this is most likely to crash the server if 'Name' is not in ``Post``. This is
where ``Voluptuous`` comes.

In ddbmock, all you need to do to enable automatic validations is to add a file
with the underscore name in ``ddbmock.validators``. It must contain a ``post``
member with the rules.

Example: HelloWorld validator for HelloWorld method:

::

    # -*- coding: utf-8 -*-
    # module: ddbmock.validators.hello_world.py

    post = {
        u'Name': unicode,
    }

Done !
