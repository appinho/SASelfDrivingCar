from sensors import setup
import time


def test_sensors():
    sensor_setup = setup.SensorSetup()
    try:
        while True:
            time.sleep(1)
            now = round(time.time() * 1000)
            sensor_setup.run(now)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    test_sensors()
