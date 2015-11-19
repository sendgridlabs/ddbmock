# -*- coding: utf-8 -*-

# Index overhead. This is added to each Item size when computing table size
INDEX_OVERHEAD = 100

# count: maximum number of tables
MAX_TABLES = 256

### items constraints ###

# bytes: max hash_key_size
MAX_HK_SIZE = 2048
# bytes: max range key size
MAX_RK_SIZE = 1024
# bytes: max item size, not including the index overhead
MAX_ITEM_SIZE = 64*1024

config = {"_default":
	{
		### throughput constraints ###
		# value: minimum throughput value
		"MIN_TP": 1,
		# value: maximum throughput value
		"MAX_TP": 10000,
		# days: min time between 2 throughtput decrease
		"MIN_TP_DEC_INTERVAL":1,
		# percent: max throughput increase per single operation
		"MAX_TP_INC_CHANGE": 100,

		### slowness simulation ###

		# boolean: enable timers ?
		"ENABLE_DELAYS": True,
		# seconds: simulate table creation delay. It will still be available immediately
		"DELAY_CREATING": 60,
		# seconds: simulate table update delay. It will still be available immediately
		"DELAY_UPDATING": 60,
		# seconds: simulate table deletion delay. It will still be available until time is exhauted
		"DELAY_DELETING": 60,

		# boolean: read-only access to tables
		"READ_ONLY": False
	},
	"admin": {},
	"read_only": {
		"READ_ONLY": True
	}
}

def config_for_user(access_key = None):
	if access_key == None:
		return config["_default"]
	else:
		user = config["_default"].copy()
		if access_key not in config:
			raise Exception, "No such user '%s'"%access_key
		user.update(config[access_key])
		return user

def setup(access_key = None):
	user = config_for_user(access_key)
	g = globals()
	for k in user.keys():
		g[k] = user[k]

setup()

### Throughput statistics ###

# seconds: datapoint duration
STAT_TP_SAMPLE = 1
# seconds: aggregation period
STAT_TP_AGGREG = 5*60

### Storage specific settings ###

# Storage engine to use ('memory' or 'sqlite')
STORAGE_ENGINE_NAME = 'memory'
# SQLite database location
STORAGE_SQLITE_FILE = 'dynamo.db'
