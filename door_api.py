# Start the API for direct door control.
from flask import Flask
import RPi.GPIO as GPIO
import threading

# constants
API_PORT = 5200

MOTOR_FORWARD = 24
MOTOR_BACKWARD = 23
MOTOR_ENABLE = 25
MOTOR_DELAY = 15  # time to run in seconds

# flask initialization
app = Flask(__name__)


# Stops the motor and runs pin cleanup
def stop_motor():
    GPIO.output(MOTOR_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_BACKWARD, GPIO.LOW)
    GPIO.cleanup()
    print("Motor stopped")


# Runs the motor, then stops it after a delay
def run_then_stop(motor_pin: int, delay: int):
    # set up the pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MOTOR_FORWARD, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(MOTOR_BACKWARD, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(MOTOR_ENABLE, GPIO.OUT, initial=GPIO.LOW)

    # not sure why this is required
    GPIO.PWM(MOTOR_ENABLE, 1000).start(100)

    # start the motor then stop it
    GPIO.output(motor_pin, GPIO.HIGH)
    threading.Timer(delay, stop_motor).start()


# Returns whether the motor is currently moving
def motor_is_moving():
    return GPIO.input(MOTOR_FORWARD) == GPIO.HIGH \
        or GPIO.input(MOTOR_BACKWARD) == GPIO.HIGH


# Open the door manually (if it isn't currently moving)
@app.route('/open', methods=['POST'])
def open_door():
    if motor_is_moving():
        print("Cannot open, door is moving!")
    else:
        print("Opening...")
        run_then_stop(MOTOR_FORWARD, MOTOR_DELAY)
    return ""  # TODO make this return something useful?


# Close the door manually (if it isn't currently moving)
@app.route('/close', methods=['POST'])
def close_door():
    if motor_is_moving():
        print("Cannot close, door is moving!")
    else:
        print("Closing...")
        run_then_stop(MOTOR_BACKWARD, MOTOR_DELAY)
    return ""  # TODO make this return something useful?


# start the api
app.run(port=API_PORT, host="0.0.0.0")
