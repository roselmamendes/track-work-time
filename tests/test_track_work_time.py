import unittest
from track_work_time.track_work_time import TrackWorkTime

class TestTrackWorkTime(unittest.TestCase):
    def test_should_save_a_work_time_unit(self):
        trackWorkTime = TrackWorkTime()
        trackWorkTime.set_track('BAU')
        actual_work_time_unit_bau = trackWorkTime.get_tracks()[0]

        self.assertEqual('BAU', actual_work_time_unit_bau.get_name())
        self.assertEqual([0,0,0,0,0], actual_work_time_unit_bau.get_periods())

    def test_should_return_a_list_of_work_time_units(self):
        trackWorkTime = TrackWorkTime()
        trackWorkTime.set_track('BAU')
        trackWorkTime.set_track('Dev')

        actual_work_time_units = trackWorkTime.get_tracks()

        self.assertEqual(2, len(actual_work_time_units))

        self.assertEqual('Dev', actual_work_time_units[1].get_name())
        self.assertEqual('BAU', actual_work_time_units[0].get_name())
