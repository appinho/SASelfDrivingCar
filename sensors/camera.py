import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

RESOLUTION = (640, 320)
# RESOLUTION = (1920, 1088)
SLEEP = 500


class CameraDriver:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = RESOLUTION
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size=RESOLUTION)
        time.sleep(0.1)
        print("Camera Driver loaded!")

    def capture(self):
        self.camera.capture(self.rawCapture, format="bgr")
        image = self.rawCapture.array
        # clear the stream in preparation for the next frame
        self.rawCapture.truncate(0)
        return image

    def show(self):
        image = self.capture()
        print(image.shape)
        cv2.imshow("Image", image)
        key = cv2.waitKey(1) & 0xFF
        # clear the stream in preparation for the next frame
        self.rawCapture.truncate(0)
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            return
