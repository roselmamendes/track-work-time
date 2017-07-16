class WorkTimeUnit:

    def __init__(self, name):
        self.periods = [0,0,0,0,0]
        self.name = name

    def get_name(self):
        return self.name

    def get_periods(self):
        return self.periods
