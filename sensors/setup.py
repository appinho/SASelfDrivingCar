from sensors import camera
from sensors import ultrasonic
import time

DELAY = 95

class SensorSetup():
    def __init__(self):
        #self.camera_driver = camera.CameraDriver()
        self.ultrasonic_drivers = [
            ultrasonic.UltrasonicDriver(31, 33), # FRONT 1
            ultrasonic.UltrasonicDriver(38, 40), # LEFT  2
            ultrasonic.UltrasonicDriver(8, 10),  # REAR  3
            ultrasonic.UltrasonicDriver(5, 7)    # RIGHT 4
        ]
        self.before = round(time.time() * 1000)
        #self.sensor_data = SensorData(self.before)
        print("Sensor Setup Init done")

    def run(self, now):
        duration = now - self.before
        if duration > DELAY:
            data = self.capture_data(now)
            self.before = round(time.time() * 1000)
            return data
        return []

    def capture_data(self, timestamp):
        #print(timestamp)
        #image = self.camera_driver.capture()
        distances = []
        for i, ultrasonic_driver in enumerate(self.ultrasonic_drivers):
            
            #ultrasonic_driver.init()
            distance = ultrasonic_driver.measure_distance()
            #print(distance)
            distances.append(distance)
            #print("Measure US Driver" , i, distance)
            #image = ultrasonic_driver.show_distance(image, distance, i)
        #cv2.imshow("Image", image)
        return timestamp, distances
        #self.sensor_data.write(timestamp, distances)
        #now = time.time()
        print("Data capture took %f ms" % (round(now * 1000) - timestamp))
        print(distances)
