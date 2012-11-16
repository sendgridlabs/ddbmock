`DynamoDB <http://aws.amazon.com/dynamodb/>`_ is a minimalistic NoSQL engine
provided by Amazon as a part of their AWS product.

**DynamoDB** allows you to store documents composed of unicode, number or binary
data as well are sets. Each tables must define a ``hash_key`` and may define a
``range_key``. All other fields are optional.

**DynamoDB** is really awesome but is terribly slooooow with managment tasks.
This makes it completly unusable in test environements.

**ddbmock** brings a nice, tiny, in-memory or sqlite implementation of
DynamoDB along with much better and detailed error messages. Among its niceties,
it features a double entry point:

 - regular network based entry-point with 1:1 correspondance with stock DynamoDB
 - **embeded entry-point** with seamless boto intergration 1, ideal to avoid spinning yet another server.

**ddbmock** is **not** intended for production use. It **will lose** your data.
you've been warned! I currently recommend the "boto extension" mode for unit-tests
and the "server" mode for functional tests.
