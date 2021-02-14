import camera
import steering
import ultrasonic

import cv2
import keyboard
import random

TIME = 0.1
counter = 0


if __name__ == "__main__":
    car = CarDriver()
    car.run()
