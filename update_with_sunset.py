import pytz
from suntime import Sun
import datetime

from api import cron

latitude = 45
longitude = -121

sun = Sun(latitude, longitude)
tz = pytz.timezone('US/Pacific')

# get open and close times based on sunrise and (sunset + 30 mins)
open_time = sun.get_sunrise_time(time_zone=tz).strftime('%H:%M')
close_time = (sun.get_sunset_time(time_zone=tz) + datetime.timedelta(minutes=30)).strftime('%H:%M')
print(f"open: {open_time} close: {close_time}")

# schedule open and close scripts at new times
cron.set_times(open_time, close_time)
