from localization import particle_filter
from navigation import keyboard_control
from navigation import parameters as nav_p
from sensors import setup
from sensors.parameters import *
import time

NUM_PARTICLES = 40
STD_V = 1.6
STD_Y = 0.3
STD_M = 0.2
X = 0.6827 + 0.1425
Y = 1.2269 + 0.09
O = 0.0


def test_data_capture():
    sensor_setup = setup.SensorSetup()
    keyboard_controller = keyboard_control.KeyboardController()
    pf = particle_filter.ParticleFilter(NUM_PARTICLES, X, Y, O)
    try:
        while True:
            now = round(time.time() * 1000)
            # Apply steering
            key = keyboard_controller.keyboard_event()
            # Get sensor data
            sensor_data = sensor_setup.run(now)
            pf.run(
                key, sensor_data, sensor_poses, nav_p.VELOCITY, nav_p.TURN_RATE
            )

    except KeyboardInterrupt:
        steering.stop(1)


if __name__ == "__main__":
    test_data_capture()
