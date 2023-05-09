import cron

# should be None
print(cron.get_open_time())
print(cron.get_close_time())

try:
    cron.set_times("nope", "nah")
    print("should not be here")
except cron.TimeFormatException as e:
    print(e.args)

try:
    cron.set_times("07:00", "21:00")
except cron.TimeFormatException as e:
    print(e.args, "should not be format exception")

print(cron.get_open_time())
print(cron.get_close_time())
