from localization import particle_filter
from navigation import keyboard_control
from sensors import setup
import time

NUM_PARTICLES = 40
STD_V = 1.6
STD_Y = 0.3
STD_M = 0.2


def test_data_capture():
    sensor_setup = setup.SensorSetup()
    keyboard_controller = keyboard_control.KeyboardController()
    pf = ParticleFilter(NUM_PARTICLES)
    try:
        while True:
            now = round(time.time() * 1000)
            # Apply steering
            key = keyboard_controller.keyboard_event()
            # Get sensor data
            sensor_data = sensor_setup.run(now)

            pf.run(key, sensor_data, VELOCITY, TURN_RATE)

    except KeyboardInterrupt:
        steering.stop(1)


if __name__ == "__main__":
    test_data_capture()
