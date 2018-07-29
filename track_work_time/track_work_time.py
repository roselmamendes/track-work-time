import logging
from track_work_time import store

logger = logging.getLogger(__name__)


class TrackWorkTime:

    def set_work_unit(self, work_unit_name):
        store.set_work_unit(work_unit_name)

    def get_work_units(self):
        return store.get_work_units()

    def set_worked_hours(self, work_unit_name, day, hours):
        minutes = hours.total_seconds()/60
        converted_hour = minutes/60

        work_unit = store.get_work_unit(work_unit_name)

        if work_unit is None:
            logger.error('It could not find the work unit %s', work_unit_name)
        else:
            store.set_week_day(day, converted_hour, work_unit)

    def get_week_hours(self, work_unit_name, start_date, end_date):
        week_days = store.get_week_days_from(work_unit_name)
        if week_days is None:
            logger.error('It could not find the work unit %s', work_unit_name)
            return []

        index_start_week = -1
        for index, week_day in enumerate(week_days):
            if week_day.day == start_date:
                index_start_week = index

        if index_start_week == -1:
            logger.error(
                'It could not find the %s for work unit %s',
                start_date,
                work_unit_name
            )
            return []

        return [
            week_days[index_start_week].hours,
            week_days[index_start_week + 1].hours,
            week_days[index_start_week + 2].hours,
            week_days[index_start_week + 3].hours,
            week_days[index_start_week + 4].hours
        ]
