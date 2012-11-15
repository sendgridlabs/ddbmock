# -*- coding: utf-8 -*-

import unittest, mock

LOGGER = 'unit-stat-test'
DELAY = 12

class TestUtils(unittest.TestCase):
    @mock.patch('ddbmock.utils.Timer')
    def test_schedule_action_enable(self, m_timer):
        from ddbmock.utils import schedule_action
        from ddbmock import config

        old_delay_param = config.ENABLE_DELAYS
        config.ENABLE_DELAYS = True

        m_cb = mock.Mock()

        schedule_action(DELAY, m_cb, ["args"], {'kwargs':'kwargs'})
        m_timer.assert_called_with(DELAY, m_cb, ["args"], {'kwargs':'kwargs'})
        m_timer.return_value.start.assert_called_with()

        config.ENABLE_DELAYS = old_delay_param

    @mock.patch('ddbmock.utils.Timer')
    def test_schedule_action_disable(self, m_timer):
        from ddbmock.utils import schedule_action
        from ddbmock import config

        old_delay_param = config.ENABLE_DELAYS
        config.ENABLE_DELAYS = False

        m_cb = mock.Mock()

        schedule_action(DELAY, m_cb, ["args"], {'kwargs':'kwargs'})
        m_cb.assert_called_with("args", kwargs='kwargs')

        config.ENABLE_DELAYS = old_delay_param

    def test_average(self):
        from ddbmock.utils.stat import average

        self.assertEqual(2, average([1,2,3]))
        self.assertEqual(2, average([1,2,3,4]))

    @mock.patch('ddbmock.utils.stat.time')
    @mock.patch('ddbmock.utils.stat.atexit')
    def test_aggregate(self, _, m_time):
        from ddbmock.utils.stat import Stat

        s = Stat(LOGGER)
        s.current_point_value = 42

        m_time.return_value = 123.5

        s._aggregate()

        self.assertEqual([42], s.current_point_list)
        self.assertEqual(0, s.current_point_value)
        self.assertEqual(123, s.current_point_time)

    @mock.patch('ddbmock.utils.stat.atexit')
    def test_macro_aggregate(self, _):
        from ddbmock.utils.stat import Stat

        s = Stat(LOGGER)

        s.current_point_list = [-4,12,5000]
        s.last_aggregation_time = 32

        s._macro_aggregate()

        self.assertEqual([], s.current_point_list)

    @mock.patch('ddbmock.utils.stat.time')
    @mock.patch('ddbmock.utils.stat.Stat._aggregate')
    @mock.patch('ddbmock.utils.stat.Stat._macro_aggregate')
    @mock.patch('ddbmock.utils.stat.atexit')
    def test_push(self, _, _m_m_agg, _m_agg, m_time):
        from ddbmock.utils.stat import Stat

        m_time.return_value = 1
        s = Stat(LOGGER)

        # nominal
        s.push(1)
        s.push(2)
        s.push(3)
        self.assertEqual(6, s.current_point_value)
        self.assertFalse(_m_agg.called)
        self.assertFalse(_m_m_agg.called)

        # manual clean (mocks...)
        s.current_point_value = 0

        # change data point
        m_time.return_value = 2.1
        s.push(4)
        self.assertEqual(4, s.current_point_value)
        self.assertTrue(_m_agg.called)
        self.assertFalse(_m_m_agg.called)

        # manual clean (mocks...)
        s.current_point_value = 0

        # change data point
        m_time.return_value = 5*60+1
        s.push(6)
        self.assertEqual(6, s.current_point_value)
        self.assertTrue(_m_agg.called)
        self.assertTrue(_m_m_agg.called)

    @mock.patch('ddbmock.utils.stat.Stat._aggregate')
    @mock.patch('ddbmock.utils.stat.Stat._macro_aggregate')
    @mock.patch('ddbmock.utils.stat.atexit')
    def test_flush(self, _, _m_m_agg, _m_agg):
        from ddbmock.utils.stat import Stat

        s = Stat(LOGGER)
        m_list = mock.MagicMock()
        s.flush()

        self.assertTrue(_m_agg.called)
        self.assertTrue(_m_m_agg.called)
