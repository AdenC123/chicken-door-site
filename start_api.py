# Start the API for direct door control.
from flask import Flask, request
import json

import cron
from door import Door

# flask initialization
app = Flask(__name__)
API_PORT = 5200

# create the door
door = Door()


@app.route('/open', methods=['POST'])
def open_door():
    """Open the door manually (if it isn't currently moving)"""
    if door.is_moving():
        # door already moving, unsuccessful
        return json.dumps({
            "success": False,
            "delay": 0
        })

    door.open()
    return json.dumps({
        "success": True,
        "delay": door.get_delay()
    })


@app.route('/close', methods=['POST'])
def close_door():
    """Close the door manually (if it isn't currently moving)"""
    if door.is_moving():
        # door already moving, unsuccessful
        return json.dumps({
            "success": False,
            "delay": 0
        })

    door.close()
    return json.dumps({
        "success": True,
        "delay": door.get_delay()
    })


@app.route('/state', methods=['GET'])
def get_state():
    return json.dumps({
        "open": door.is_open(),
        "moving": door.is_moving(),
        "openTime": cron.get_open_time(),
        "closeTime": cron.get_close_time()
    })


@app.route('/times', methods=['POST'])
def set_times():
    """Set the open and close times in cron."""
    open_time = request.form.get("openTime")
    close_time = request.form.get("closeTime")
    if open_time is None:
        return json.dumps({"error": "Request data does not contain openTime"})
    if close_time is None:
        return json.dumps({"error": "Request data does not contain closeTime"})
    try:
        cron.set_times(open_time, close_time)
        return json.dumps({"success": True})
    except cron.TimeFormatException as e:
        msg = "Time is in incorrect format: " + e.args[0]
        return json.dumps({"error": msg})


# start the api
app.run(port=API_PORT, host="0.0.0.0")
