import io
import socket
import struct
import time
import pickle

from data.data_writer import DataWriter
from navigation import keyboard_control
from navigation.parameters import VELOCITY, TURN_RATE
from network.parameters import ip_address, port
from localization.particle_filter import ParticleFilter
from sensors.setup import SensorSetup
from sensors.parameters import sensor_poses


def live_demo_localization():
    client_socket = socket.socket()
    client_socket.connect((ip_address, port))

    keyboard_controller = keyboard_control.KeyboardController()
    sensor_setup = SensorSetup()

    now = time.time()
    data_write = DataWriter(now)
    print("Write log to %f.txt" % now)

    start_x = 0.5
    start_y = 1.3
    start_o = 0.0
    pf = ParticleFilter(x=start_x, y=start_y, o=start_o)
    try:
        while True:
            now = round(time.time() * 1000)
            steering = keyboard_controller.keyboard_event()
            sensor_data = sensor_setup.run(now)
            if sensor_data:
                data_write.write(sensor_data[0], sensor_data[1], steering)
            best_index = pf.run(steering, sensor_data,
                                sensor_poses, VELOCITY, TURN_RATE)
            if not best_index:
                continue
            best_particle = pf.particles[best_index]
            data_string = pickle.dumps(best_particle)
            client_socket.send(data_string)
            data = client_socket.recv(1024)
            if steering == "Q":
                break
    except KeyboardInterrupt:
        pass
    finally:
        client_socket.close()


if __name__ == "__main__":
    live_demo_localization()
