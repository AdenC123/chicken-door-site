# Start the API for direct door control.
from flask import Flask
import RPi.GPIO as GPIO
import threading

# constants
API_PORT = 5200

MOTOR_FORWARD = 24
MOTOR_BACKWARD = 23
# MOTOR_ENABLE = 25
MOTOR_DELAY = 10  # time to run in seconds

# flask initialization
app = Flask(__name__)

# motor setup with ports
GPIO.setmode(GPIO.BCM)
GPIO.setup(MOTOR_FORWARD, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(MOTOR_BACKWARD, GPIO.OUT, initial=GPIO.LOW)


# Stops the motor
def stop_motor():
    GPIO.output(MOTOR_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_BACKWARD, GPIO.LOW)
    print("Motor stopped")


# Stops the motor after a delay
def stop_after(delay: int):
    threading.Timer(delay, stop_motor).start()


# Returns whether the motor is currently moving
def motor_is_moving():
    return GPIO.input(MOTOR_FORWARD) or GPIO.input(MOTOR_BACKWARD)


# Open the door manually (if it isn't currently moving)
@app.route('/open', methods=['POST'])
def open_door():
    if motor_is_moving():
        print("Door is moving!")
    else:
        print("Opening...")
        GPIO.output(MOTOR_FORWARD, GPIO.HIGH)
        stop_after(MOTOR_DELAY)
    return ""


# Close the door manually (if it isn't currently moving)
@app.route('/close', methods=['POST'])
def close_door():
    if motor_is_moving():
        print("Door is moving!")
    else:
        print("Closing...")
        GPIO.output(MOTOR_BACKWARD, GPIO.HIGH)
        stop_after(MOTOR_DELAY)
    return ""


# start the api
app.run(port=API_PORT, host="0.0.0.0")
