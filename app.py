from flask import Flask, render_template, request
import subprocess
from threading import Timer

# delay time before allowing door to open or close again
DELAY_TIME = 12

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
    return render_template('Home.html')


if __name__ == '__main__':
    app.run(port=5100, host="0.0.0.0")
