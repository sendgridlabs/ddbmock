# -*- coding: utf-8 -*-

# automagically runs boto DynamoDB integration tests

import os, imp, boto
from ddbmock import connect_boto_patch

# Load boto dir
boto_dir = os.path.realpath(boto.__file__+'/../../')

# Plug patch
connect_boto_patch()

# Import boto test modules, pretending they are belonging to us. see hack in tests.unit.__init__
layer1_file, _, desc1 = imp.find_module('test_layer1', [boto_dir+'/tests/integration/dynamodb'])
layer2_file, _, desc2 = imp.find_module('test_layer2', [boto_dir+'/tests/integration/dynamodb'])
layer1_module = imp.load_module('test_layer1', layer1_file, boto_dir, desc1)
layer2_module = imp.load_module('test_layer2', layer2_file, boto_dir, desc2)

# Finally, import the test class, that enough to let the magic happen !
DynamoDBLayer1Test = layer1_module.DynamoDBLayer1Test
DynamoDBLayer2Test = layer2_module.DynamoDBLayer2Test
