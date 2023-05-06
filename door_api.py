# Start the API for direct door control.
from flask import Flask
from gpiozero import Motor
import threading


# constants
API_PORT = 5200

MOTOR_FORWARD = 23
MOTOR_BACKWARD = 24
MOTOR_ENABLE = 25
MOTOR_DELAY = 5  # time to run in seconds

# flask initialization
app = Flask(__name__)

# motor setup with ports
motor = Motor(MOTOR_FORWARD, MOTOR_BACKWARD, MOTOR_ENABLE)


# Stops the motor
def stop_motor():
    motor.stop()
    print("Motor stopped")


# Stops the motor after a delay
def stop_after(delay: int):
    threading.Timer(delay, stop_motor).start()


# Open the door manually (if it isn't currently moving)
@app.route('/open', methods='POST')
def open_door():
    if motor.is_active:
        print("Door already open!")
    else:
        print("Opening...")
        motor.forward()
        stop_after(MOTOR_DELAY)


# Close the door manually (if it isn't currently moving)
@app.route('/close', methods='POST')
def close_door():
    if motor.is_active:
        print("Door already closed!")
    else:
        print("Closing...")
        motor.backward()
        stop_after(MOTOR_DELAY)


# start the api
app.run(port=API_PORT, host="0.0.0.0")