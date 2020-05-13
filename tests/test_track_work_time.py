from unittest import TestCase, mock
from datetime import date, timedelta
from track_work_time.track_work_time import TrackWorkTime
from track_work_time import store


class TestTrackWorkTime(TestCase):

    def setUp(self):
        self.store = Store('sqlite:///test.db')
        self.store.delete_all_on_db()

    def tearDown(self):
        self.store.delete_all_on_db()
        self.store.close_session()

    def test_should_save_a_work_unit(self):
        track = TrackWorkTime()
        track.set_work_unit('BAU')

        actual_work_time_unit_bau = track.get_work_units()[0]

        self.assertEqual('BAU', actual_work_time_unit_bau.name)
        self.assertEqual([], actual_work_time_unit_bau.weekdays)

    def test_should_return_a_list_of_work_units(self):
        track = TrackWorkTime()
        track.set_work_unit('BAU')
        track.set_work_unit('Dev')

        actual_work_time_units = track.get_work_units()

        self.assertEqual(2, len(actual_work_time_units))

        self.assertEqual('Dev', actual_work_time_units[1].name)
        self.assertEqual('BAU', actual_work_time_units[0].name)

    def test_should_get_a_week_of_a_month(self):
        track = TrackWorkTime()
        track.set_work_unit('BAU')

        track.set_worked_hours(
            'BAU', date(2017, 7, 10), timedelta(hours=4))
        track.set_worked_hours(
            'BAU', date(2017, 7, 11), timedelta(hours=4))
        track.set_worked_hours(
            'BAU', date(2017, 7, 12), timedelta(hours=4))
        track.set_worked_hours(
            'BAU', date(2017, 7, 13), timedelta(hours=4))
        track.set_worked_hours(
            'BAU', date(2017, 7, 14), timedelta(hours=4))

        self.assertEqual(
            [4.0, 4.0, 4.0, 4.0, 4.0],
            track.get_week_hours(
                'BAU', date(2017, 7, 10)
            )
        )

    @mock.patch('track_work_time.track_work_time.logger.error')
    def test_return_empty_list_when_did_not_find_work_unit(self, log_error):
        track = TrackWorkTime()

        actual_week_hours = track.get_week_hours(
            'BAU', date(2017, 7, 10)
        )

        log_error.assert_called_once_with(
            'It could not find the week of %s for work unit %s',
            date(2017, 7, 10),
            'BAU'
        )
        self.assertEqual([], actual_week_hours)

    @mock.patch('track_work_time.track_work_time.logger.error')
    def test_return_empty_list_when_did_not_find_week_day(self, log_error):
        track = TrackWorkTime()
        store.set_work_unit('BAU')

        actual_week_hours = track.get_week_hours(
            'BAU', date(2017, 7, 10)
        )

        log_error.assert_called_once_with(
            'It could not find the week of %s for work unit %s',
            date(2017, 7, 10),
            'BAU'
        )
        self.assertEqual([], actual_week_hours)

    @mock.patch('track_work_time.track_work_time.logger.error')
    def test_set_worked_hours_call_log_error_when_didnt_find_work_unit(
            self, log_error
    ):
        track = TrackWorkTime()

        track.set_worked_hours('BAU', date(2017, 6, 21), timedelta(hours=2))

        log_error.assert_called_once_with('It could not find the work unit %s',
                                          'BAU')

    def test_should_find_the_week_hours_even_for_not_completed_week(
            self
    ):
        track = TrackWorkTime()

        track.set_work_unit('App Dev')
        track.set_worked_hours(
            'App Dev', date(2017, 7, 11), timedelta(hours=4))
        track.set_worked_hours(
            'App Dev', date(2017, 7, 12), timedelta(hours=4))

        self.assertEqual(
            [0, 4.0, 4.0, 0, 0],
            track.get_week_hours(
                'App Dev', date(2017, 7, 10)
            )
        )
