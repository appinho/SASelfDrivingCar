import cv2
import RPi.GPIO as gpio
import time


class UltrasonicDriver:
    def __init__(self, pin_trigger, pin_echo):
        self.pin_trigger = pin_trigger
        self.pin_echo = pin_echo
        self.init()

    def init(self):
        gpio.setmode(gpio.BOARD)
        gpio.setup(self.pin_trigger, gpio.OUT)
        gpio.setup(self.pin_echo, gpio.IN)

    def show_distance(self, image, distance=None, index=0):
        if distance is None:
            distance = self.measure_distance()
        text = "%2.4f cm" % distance
        org = (0, (index + 1) * 50)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 2
        color = (255, 0, 0)
        thickness = 2
        cv2.putText(
            image, text, org, font, font_scale, color, thickness, cv2.LINE_AA
        )
        return image

    def measure_distance(self, measure="cm"):
        self.init()
        time.sleep(0.005)
        gpio.output(self.pin_trigger, True)
        time.sleep(0.00001)
        gpio.output(self.pin_trigger, False)
        while gpio.input(self.pin_echo) == 0:
            nosig = time.time()
        while gpio.input(self.pin_echo) == 1:
            sig = time.time()
        tl = sig - nosig

        if measure == "cm":
            distance = tl / 0.000058
        elif measure == "in":
            distance = tl / 0.000148
        else:
            print("Improper choice of measurement: in or cm")
            distance = None

        # gpio.cleanup()
        return distance

    def test(self):
        for i in range(100):
            print("Measurement %d: %2.4f cm" % (i, self.measure_distance("cm")))
            time.sleep(0.5)


# us = UltrasonicDriver(5,7)
# us.test()
