import RPi.GPIO as gpio
import time

PIN_MOTOR_FRONT_LEFT = 22
PIN_MOTOR_FRONT_RIGHT = 24
PIN_MOTOR_REAR_LEFT = 26
PIN_MOTOR_REAR_RIGHT = 18

def init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(PIN_MOTOR_FRONT_LEFT, gpio.OUT)
    gpio.setup(PIN_MOTOR_FRONT_RIGHT, gpio.OUT)
    gpio.setup(PIN_MOTOR_REAR_LEFT, gpio.OUT)
    gpio.setup(PIN_MOTOR_REAR_RIGHT, gpio.OUT)

def turn_right(tf):
    gpio.output(PIN_MOTOR_FRONT_LEFT, False)
    gpio.output(PIN_MOTOR_FRONT_RIGHT, True)
    gpio.output(PIN_MOTOR_REAR_LEFT, False)
    gpio.output(PIN_MOTOR_REAR_RIGHT, True)
    time.sleep(tf)
    
def turn_left(tf):
    gpio.output(PIN_MOTOR_FRONT_LEFT, True)
    gpio.output(PIN_MOTOR_FRONT_RIGHT, False)
    gpio.output(PIN_MOTOR_REAR_LEFT, True)
    gpio.output(PIN_MOTOR_REAR_RIGHT, False)
    time.sleep(tf)
    
def forward(tf):
    gpio.output(PIN_MOTOR_FRONT_LEFT, True)
    gpio.output(PIN_MOTOR_FRONT_RIGHT, False)
    gpio.output(PIN_MOTOR_REAR_LEFT, False)
    gpio.output(PIN_MOTOR_REAR_RIGHT, True)
    time.sleep(tf)
    
def reverse(tf):
    gpio.output(PIN_MOTOR_FRONT_LEFT, False)
    gpio.output(PIN_MOTOR_FRONT_RIGHT, True)
    gpio.output(PIN_MOTOR_REAR_LEFT, True)
    gpio.output(PIN_MOTOR_REAR_RIGHT, False)
    time.sleep(tf)

def stop(tf):
    gpio.output(PIN_MOTOR_FRONT_LEFT, False)
    gpio.output(PIN_MOTOR_FRONT_RIGHT, False)
    gpio.output(PIN_MOTOR_REAR_LEFT, False)
    gpio.output(PIN_MOTOR_REAR_RIGHT, False)
    time.sleep(tf)
    #gpio.cleanup()
