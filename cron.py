import re

from crontab import CronTab

OPEN_COMMAND = "curl -X POST 127.0.0.1:5200/open"
CLOSE_COMMAND = "curl -X POST 127.0.0.1:5200/close"


class TimeFormatException(Exception):
    """Times are in the incorrect format. First argument is the offending time."""


def set_times(open_time: str, close_time: str):
    """Set the times for the door to open and close in cron."""
    _set_time_with_command(open_time, OPEN_COMMAND)
    _set_time_with_command(close_time, CLOSE_COMMAND)


def get_open_time():
    """Get the current opening time from cron, or None if there is no time."""
    return _get_time_with_command(OPEN_COMMAND)


def get_close_time():
    """Get the current closing time from cron, or None if there is no time."""
    return _get_time_with_command(CLOSE_COMMAND)


def _set_time_with_command(time: str, command: str):
    # check format of times: must be exactly 4 digits
    if not re.search(r'^\d{2}:\d{2}$', time):
        raise TimeFormatException(time)
    # convert time to hours and minutes
    hour = int(time[0:2])
    minute = int(time[2:4])
    if hour >= 24 or minute >= 60:
        raise TimeFormatException(time)

    with CronTab(user=True) as cron:
        job = None
        try:
            # use the first job with the command
            job = next(cron.find_command(command=command))
        except StopIteration:
            # no job with given command exists, need to create it
            job = cron.new(command=command)
        # assign times
        job.hour.on(hour)
        job.minute.on(minute)


def _get_time_with_command(command: str):
    with CronTab(user=True) as cron:
        try:
            job = next(cron.find_command(command=command))
        except StopIteration:
            return None
        return str(job.hour) + ":" + str(job.minute)
