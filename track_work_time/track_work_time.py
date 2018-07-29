import logging
from track_work_time import store
from datetime import timedelta
logger = logging.getLogger(__name__)


class TrackWorkTime:

    def set_work_unit(self, work_unit_name):
        store.set_work_unit(work_unit_name)

    def get_work_units(self):
        return store.get_work_units()

    def set_worked_hours(self, work_unit_name, day, hours):
        converted_hour = self._obtain_converted_hour(hours)

        work_unit = store.get_work_unit(work_unit_name)

        if work_unit is None:
            logger.error('It could not find the work unit %s', work_unit_name)
        else:
            store.set_week_day(day, converted_hour, work_unit)

    def _obtain_converted_hour(self, hours):
        minutes = hours.total_seconds()/60
        return minutes/60

    def get_week_hours(self, work_unit_name, week_monday):
        if self._is_monday(week_monday):
            logger.error('Inform a monday date to get the hours for a '
                         + 'specific week.', work_unit_name)
            return []

        week_days = self._get_week_days_from_db(work_unit_name, week_monday)

        if not week_days:
            logger.error(
                'It could not find the week of %s for work unit %s',
                week_monday,
                work_unit_name
            )
            return []

        return self._get_week_hours(week_days)

    def _is_monday(self, day):
        return day.weekday() != 0

    def _get_week_days_from_db(self, work_unit_name, week_monday):
        week_friday = week_monday + timedelta(days=4)

        return store.get_week_days_from(
            work_unit_name,
            week_monday,
            week_friday
        )

    def _get_week_hours(self, week_days):
        week_days_to_be_returned = []

        for week_index in range(0, 5):
            hours = self._get_hours_from_week_index(week_index, week_days)

            week_days_to_be_returned.append(hours)

        return week_days_to_be_returned

    def _get_hours_from_week_index(self, week_index, week_days):
        hours = 0
        for week_day in week_days:
            if week_day.day.weekday() == week_index:
                hours = week_day.hours
                break

        return hours
