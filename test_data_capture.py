from data import data_writer
from navigation import run
from navigation import keyboard_control
from sensors import setup
import time

AUTONOMOUS = False


def test_data_capture():
    sensor_setup = setup.SensorSetup()
    data_write = data_writer.DataWriter(time.time())
    if AUTONOMOUS:
        # TODO
        car_setup = run.Drive()
    else:
        keyboard_controller = keyboard_control.KeyboardController()

    try:
        while True:
            now = round(time.time() * 1000)
            # Apply steering
            if AUTONOMOUS:
                # TODO
                car_setup = run.Drive()
            else:
                key = keyboard_controller.keyboard_event()
            # Get sensor data
            sensor_data = sensor_setup.run(now)

            if sensor_data:
                data_write.write(sensor_data[0], sensor_data[1], key)
            if key == "Q":
                break
    except KeyboardInterrupt:
        pass  # steering.stop(1)


if __name__ == "__main__":
    test_data_capture()
