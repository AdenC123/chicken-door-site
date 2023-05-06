import threading
import RPi.GPIO as GPIO
import time

MOTOR_FORWARD = 24
MOTOR_BACKWARD = 23
MOTOR_ENABLE = 25
MOTOR_DELAY = 15  # time to run in seconds


def _setup_pins_output():
    # print("setting up pins")
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(MOTOR_FORWARD, GPIO.OUT)
    # GPIO.setup(MOTOR_BACKWARD, GPIO.OUT)
    # GPIO.setup(MOTOR_ENABLE, GPIO.OUT)
    # # not sure why this is required
    # GPIO.PWM(MOTOR_ENABLE, 1000).start(100)

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MOTOR_FORWARD, GPIO.OUT)
    GPIO.setup(MOTOR_BACKWARD, GPIO.OUT)
    GPIO.setup(MOTOR_ENABLE, GPIO.OUT)
    GPIO.output(MOTOR_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_BACKWARD, GPIO.LOW)

    p = GPIO.PWM(MOTOR_ENABLE, 1000)
    p.start(100)


class Door:
    def __init__(self):
        """Creates the Door that is not moving and stops it"""
        # set up fields
        self._is_moving = False
        self._is_open = None  # unknown state when app starts

        # self._setup_pins_output()
        # self._stop_motor()

    def open(self):
        """Opens the door and stops the motor"""
        self._is_moving = True
        self._is_open = True

        _setup_pins_output()
        GPIO.output(MOTOR_FORWARD, GPIO.HIGH)
        threading.Timer(MOTOR_DELAY, self._stop_motor).start()

    def close(self):
        """Closes the door and stops the motor"""
        # self._is_moving = True
        # self._is_open = False
        #
        # self._setup_pins_output()
        # GPIO.output(MOTOR_FORWARD, GPIO.LOW)
        # GPIO.output(MOTOR_BACKWARD, GPIO.HIGH)
        # threading.Timer(MOTOR_DELAY, self._stop_motor).start()
        # print("done closing in door")

        _setup_pins_output()

        # run motor backward for 10 seconds
        GPIO.output(MOTOR_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_BACKWARD, GPIO.HIGH)
        time.sleep(20)
        GPIO.output(MOTOR_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_BACKWARD, GPIO.LOW)
        GPIO.cleanup()

    def is_moving(self):
        """Returns whether the door is currently moving"""
        return self._is_moving

    def is_open(self):
        """Returns whether the door is currently open, or None if unknown"""
        return self._is_open

    # Sets up the pins to move the motor, should be cleaned up after use

    # Stops the motor and runs pin cleanup
    # Requires pins to be set up
    def _stop_motor(self):
        GPIO.output(MOTOR_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_BACKWARD, GPIO.LOW)
        GPIO.cleanup()
        self._is_moving = False
        print('Motor stopped')  # TODO remove?
