# Start the API for direct door control.
from flask import Flask

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
        return "Cannot open, door is moving!"

    door.open()
    return "Opening..."


# Close the door manually (if it isn't currently moving)
@app.route('/close', methods=['POST'])
def close_door():
    if door.is_moving():
        return "Cannot close, door is moving!"

    door.close()
    return "Closing..."


# start the api
app.run(port=API_PORT, host="0.0.0.0")
