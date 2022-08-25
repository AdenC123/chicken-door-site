from flask import Flask, render_template, request
import subprocess
from threading import Timer
from crontab import CronTab
import re

# delay time before allowing door to open or close again
DELAY_TIME = 10

# paths to open and close files
OPEN_PATH = "/home/pi/Documents/PythonStuff/open.py"
CLOSE_PATH = "/home/pi/Documents/PythonStuff/close.py"
# keep track if door is active
door_active = False


def door_done():
    global door_active
    door_active = False
    print("door active again")


def manual_open():
    global door_active
    if not door_active:
        door_active = True
        print("opening...")
        subprocess.call(['python3', OPEN_PATH])
        t = Timer(DELAY_TIME, door_done)
        t.start()


def manual_close():
    global door_active
    if not door_active:
        door_active = True
        print("closing...")
        subprocess.call(['python3', CLOSE_PATH])
        t = Timer(DELAY_TIME, door_done)
        t.start()


# flask stuff
app = Flask(__name__)


# default page
@app.route('/')
def index():
    return render_template('Home.html')


# url to open door manually
@app.route('/open')
def opens():
    manual_open()
    return render_template('Home.html')


# url to close door manually
@app.route('/close')
def closes():
    manual_close()
    return render_template('Home.html')


# edit cron file
@app.route('/send_times', methods=['POST'])
def update_times():
    open_time = request.form['open-time']
    close_time = request.form['close-time']
    print(open_time)
    print(close_time)

    # make sure times are the right format
    for time in open_time, close_time:
        if not re.search('\d\d\d\d', time):
            return render_template('Home.html')

    # store times by hour and min
    open_hour = int(open_time[0:2])
    open_minute = int(open_time[2:4])
    close_hour = int(close_time[0:2])
    close_minute = int(close_time[2:4])

    # write times to cron
    with CronTab(user=True) as cron:
        open_job = next(cron.find_comment('open door'))
        open_job.hour.on(open_hour)
        open_job.minute.on(open_minute)
        close_job = next(cron.find_comment('close door'))
        close_job.hour.on(close_hour)
        close_job.minute.on(close_minute)

    return render_template('Home.html')


if __name__ == '__main__':
    app.run(port=5100, host="0.0.0.0")
