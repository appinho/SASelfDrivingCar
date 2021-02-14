from navigation import run
from sensors import setup
import time

def test_data_capture():
    sensor_setup = setup.SensorSetup()
    car_setup = run.Drive()
    
    try:
        while(True):
            time.sleep(1)
            now = round(time.time() * 1000)
            
            sensor_setup.run(now)
            stop = car_setup.run(now)
            if stop:
                break
    except KeyboardInterrupt:
        pass #steering.stop(1)

if __name__ == "__main__":
    test_data_capture()
