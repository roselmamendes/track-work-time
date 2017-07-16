from track_work_time.week_day import WeekDay

class WorkUnit:

    def __init__(self, name):
        self.periods = []
        self.name = name

    def get_name(self):
        return self.name

    def get_week_days(self):
        return self.periods

    def set_week_day(self, day, hours):
        self.periods.append(WeekDay(day, hours))
