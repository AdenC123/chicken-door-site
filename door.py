import threading
import RPi.GPIO as GPIO
import time

MOTOR_FORWARD = 24
MOTOR_BACKWARD = 23
MOTOR_ENABLE = 25
MOTOR_DELAY = 15  # time to run in seconds


class Door:
    def __init__(self):
        """Creates the Door that is not moving and stops it"""
        # set up fields
        self._is_moving = False
        self._is_open = None  # unknown state when app starts

    def open(self):
        """Opens the door and stops the motor"""
        self._is_open = True
        threading.Thread(target=self._thread_run_motor, args=[MOTOR_FORWARD]).start()

    def close(self):
        """Closes the door and stops the motor"""
        self._is_open = False
        threading.Thread(target=self._thread_run_motor, args=[MOTOR_BACKWARD]).start()

    def is_moving(self):
        """Returns whether the door is currently moving"""
        return self._is_moving

    def is_open(self):
        """Returns whether the door is currently open, or None if unknown"""
        return self._is_open

    def get_delay(self):
        """Returns the amount of time the motor runs for when opening/closing"""
        return MOTOR_DELAY

    def _thread_run_motor(self, pin: int):
        """Sets pin to HIGH for MOTOR_DELAY seconds, then stops the motor."""
        self._is_moving = True
        # set up pins and pwm
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(MOTOR_FORWARD, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(MOTOR_BACKWARD, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(MOTOR_ENABLE, GPIO.OUT, initial=GPIO.LOW)
        p = GPIO.PWM(MOTOR_ENABLE, 1000)
        p.start(100)
        # run motor
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(MOTOR_DELAY)
        # stop
        GPIO.output(MOTOR_FORWARD, GPIO.LOW)
        GPIO.output(MOTOR_BACKWARD, GPIO.LOW)
        GPIO.cleanup()
        self._is_moving = False
        print("motor stopped")


