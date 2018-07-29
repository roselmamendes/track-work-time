from unittest import TestCase, mock
from datetime import date, timedelta
from track_work_time.track_work_time import TrackWorkTime


class TestTrackWorkTime(TestCase):
    def test_should_save_a_work_unit(self):
        trackWorkTime = TrackWorkTime()
        trackWorkTime.set_work_unit('BAU')
        actual_work_time_unit_bau = trackWorkTime.get_work_units()[0]

        self.assertEqual('BAU', actual_work_time_unit_bau.get_name())
        self.assertEqual([], actual_work_time_unit_bau.get_week_days())

    def test_should_return_a_list_of_work_units(self):
        trackWorkTime = TrackWorkTime()
        trackWorkTime.set_work_unit('BAU')
        trackWorkTime.set_work_unit('Dev')

        actual_work_time_units = trackWorkTime.get_work_units()

        self.assertEqual(2, len(actual_work_time_units))

        self.assertEqual('Dev', actual_work_time_units[1].get_name())
        self.assertEqual('BAU', actual_work_time_units[0].get_name())

    def test_should_get_a_week_of_a_month(self):
        trackWorkTime = TrackWorkTime()
        trackWorkTime.set_work_unit('BAU')

        trackWorkTime.set_worked_hours(
            'BAU', date(2017, 7, 10), timedelta(hours=4))
        trackWorkTime.set_worked_hours(
            'BAU', date(2017, 7, 11), timedelta(hours=4))
        trackWorkTime.set_worked_hours(
            'BAU', date(2017, 7, 12), timedelta(hours=4))
        trackWorkTime.set_worked_hours(
            'BAU', date(2017, 7, 13), timedelta(hours=4))
        trackWorkTime.set_worked_hours(
            'BAU', date(2017, 7, 14), timedelta(hours=4))

        self.assertEqual(
            [4.0, 4.0, 4.0, 4.0, 4.0],
            trackWorkTime.get_week_hours(
                'BAU', date(2017, 7, 10), date(2017, 7, 14)
            )
        )

    @mock.patch('track_work_time.track_work_time.logger.error')
    def test_return_empty_list_when_did_not_find_work_unit(self, log_error):
        trackWorkTime = TrackWorkTime()

        actual_week_hours = trackWorkTime.get_week_hours(
            'BAU', date(2017, 7, 10), date(2017, 7, 14)
        )

        log_error.assert_called_once_with(
            'It could not find the work unit %s', 'BAU'
        )
        self.assertEqual([], actual_week_hours)

    @mock.patch('track_work_time.track_work_time.logger.error')
    def test_return_empty_list_when_did_not_find_week_day(self, log_error):
        trackWorkTime = TrackWorkTime()
        trackWorkTime.set_work_unit('BAU')

        actual_week_hours = trackWorkTime.get_week_hours(
            'BAU', date(2017, 7, 10), None
        )

        log_error.assert_called_once_with(
            'It could not find the %s for work unit %s',
            date(2017, 7, 10),
            'BAU'
        )
        self.assertEqual([], actual_week_hours)

    @mock.patch('track_work_time.track_work_time.logger.error')
    def test_set_worked_hours_call_log_error_when_didnt_find_work_unit(
            self, log_error
    ):
        trackWorkTime = TrackWorkTime()

        trackWorkTime.set_worked_hours('BAU', None, timedelta(hours=2))

        log_error.assert_called_once_with('It could not find the work unit %s',
                                          'BAU')
