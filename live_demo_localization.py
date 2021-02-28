import io
import socket
import struct
import time
from navigation import keyboard_control


def live_demo_localization():
	client_socket = socket.socket()
	client_socket.connect((ip_address, port))

	keyboard_controller = keyboard_control.KeyboardController()

	start_x = 0.5
	start_y = 1.3
	start_o = 0.0
	pf = particle_filter.ParticleFilter(x=start_x, y=start_y, o=start_o)
	try:
        while True:
            now = round(time.time() * 1000)
			key = keyboard_controller.keyboard_event()
			sensor_data = sensor_setup.run(now)
			if sensor_data:
				s.sendall(b'S' + str(sensor_data[0]))
				data = s.recv(1024)
			if key == "Q":
                break
    except KeyboardInterrupt:
        pass
	finally:
		client_socket.close()

if __name__ == "__main__":
    live_demo_localization()
