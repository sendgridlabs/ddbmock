# -*- coding: utf-8 -*-

from ddbmock import config

# Much too slow otherwise
config.DELAY_CREATING = 0.01
config.DELAY_UPDATING = 0.01
config.DELAY_DELETING = 0.01
