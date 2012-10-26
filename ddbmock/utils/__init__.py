# -*- coding: utf-8 -*-

from .stat import Stat
from ddbmock import config

perf_logger = {
    'read': {},
    'write': {},
}

def push_read_throughput(table_name, value):
    if table_name not in perf_logger['read']:
        perf_logger['read'][table_name] = Stat("`%s` read throughput" % table_name,
                                               config.STAT_TP_SAMPLE,
                                               config.STAT_TP_AGGREG)
    perf_logger['read'][table_name].push(value)

def push_write_throughput(table_name, value):
    if table_name not in perf_logger['write']:
        perf_logger['write'][table_name] = Stat("`%s` write throughput" % table_name,
                                                config.STAT_TP_SAMPLE,
                                                config.STAT_TP_AGGREG)
    perf_logger['write'][table_name].push(value)
