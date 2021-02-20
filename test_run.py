from navigation import parameters
from navigation import steering

"""
This script lets the robot car drive in a rectangle of shape 4m x 1m:

		v-------Start|End-------<
		|						|
		|						|
		|						|
		>_______________________^
"""


def test_run():
    steering.init()
    steering.forward(2 * parameters.TTT_1M)
    steering.turn_right(parameters.TTT_90DEG)
    steering.forward(parameters.TTT_1M)
    steering.turn_right(parameters.TTT_90DEG)
    steering.forward(4 * parameters.TTT_1M)
    steering.turn_right(parameters.TTT_90DEG)
    steering.forward(parameters.TTT_1M)
    steering.turn_right(parameters.TTT_90DEG)
    steering.forward(2 * parameters.TTT_1M)
    steering.stop(1)


if __name__ == "__main__":
    test_run()
