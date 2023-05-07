# Start the API for direct door control.
from flask import Flask
import json

from door import Door


# flask initialization
app = Flask(__name__)
API_PORT = 5200

# create the door
door = Door()


# Open the door manually (if it isn't currently moving)
@app.route('/open', methods=['POST'])
def open_door():
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


# Close the door manually (if it isn't currently moving)
@app.route('/close', methods=['POST'])
def close_door():
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


# start the api
app.run(port=API_PORT, host="0.0.0.0")
