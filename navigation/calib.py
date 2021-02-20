import steering
import time

# 92cm / 3 = 30.5 cm/s
# 240 degree = 80 deg/s = 4.19rad/s
WAIT = 3
print("START")
steering.init()

# steering.stop(1)
steering.forward(WAIT)
steering.reverse(WAIT)
steering.turn_right(WAIT)
steering.turn_left(WAIT)
steering.stop(1)
print("END")
