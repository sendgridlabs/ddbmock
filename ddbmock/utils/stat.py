# -*- coding: utf-8 -*-

from time import time, ctime
from collections import namedtuple
import atexit


DataPoint = namedtuple('DataPoint', ['id', 'average', 'min', 'max'])

def average(data):
    return sum(data)/len(data)

class Stat(object):
    def __init__(self, name, resolution_interval=1, aggregation_interval=5*60):
        """
        :param name: name of the measured parameter
        :param resolution_interval: all data accumulated in this slot are part of the same point
        :param aggregation_interval: aggregates data on this period
        """

        # Load params
        self.name = name
        self.resolution_interval = resolution_interval
        self.aggregation_interval = aggregation_interval

        # Set internal state
        self.current_point_id = int(time())
        self.current_point_list = []
        self.current_point_value = 0

        # macro points
        self.aggregated_points_id = self.current_point_id
        self.aggregated_points_list = []

        # goodbye
        atexit.register(self.flush)

    def _macro_aggregate(self):
        """Perform aggregation every aggregation_interval"""
        # aggregate
        points = self.current_point_list

        d = DataPoint(id=self.aggregated_points_id,
                      min=min(points),
                      max=max(points),
                      average=average(points))

        self.aggregated_points_list.append(d)

        #reset
        self.current_point_list = []
        self.aggregated_points_id = self.current_point_id

    def _aggregate(self):
        """Trigger aggregation and reset current data"""
        # aggregate
        self.current_point_list.append(self.current_point_value)

        # reset
        self.current_point_value = 0
        self.current_point_id = int(time())


    def push(self, value):
        """Push a data point

        :param value: value to push
        """
        current_time = int(time())

        # aggregate ?
        if self.current_point_id + self.resolution_interval < current_time:
            self._aggregate()
        if self.aggregated_points_id + self.aggregation_interval < current_time:
            self._macro_aggregate()

        # update value
        self.current_point_value += value

    def flush(self):
        """Force all aggregations, reset internal state and print the results
        """

        self._aggregate()
        self._macro_aggregate()

        print "\nStatistics for '%s':" % self.name

        for point in self.aggregated_points_list:
            print "\t{}: min={}, max={}, average={}".format(ctime(point.id),
                                                          point.min,
                                                          point.max,
                                                          point.average)

        self.current_point_list = []

