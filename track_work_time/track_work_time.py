from track_work_time.work_time_unit import WorkTimeUnit

class TrackWorkTime:

    def __init__(self):
        self.tracks = []

    def set_track(self, name):
        self.tracks.append(WorkTimeUnit(name))

    def get_tracks(self):
        return self.tracks
