# Start the API for direct door control.
from flask import Flask
import json

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
        "openTime": 0000,  # TODO get these from cron module
        "closeTime": 0000
    })


# start the api
app.run(port=API_PORT, host="0.0.0.0")
