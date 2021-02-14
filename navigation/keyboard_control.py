from . import steering
import keyboard

sleep_time = 0.060 #s

class KeyboardController():
    def __init__(self):
        steering.init()
        # Assuming the bot is paused in the beginning
        self.last_input = "P"

    def keyboard_event(self):
        if keyboard.is_pressed("w"):
            print("W")
            steering.forward(sleep_time)
            self.last_input = "W"
        elif keyboard.is_pressed("a"):
            print("A")
            steering.turn_left(sleep_time)
            self.last_input = "A"
        elif keyboard.is_pressed("s"):
            print("S")
            steering.reverse(sleep_time)
            self.last_input = "S"
        elif keyboard.is_pressed("d"):
            print("D")
            steering.turn_right(sleep_time)
            self.last_input = "D"
        elif keyboard.is_pressed("p"):
            print("P")
            steering.stop(sleep_time)
            self.last_input = "P"
        elif keyboard.is_pressed("q"):
            steering.stop(sleep_time)
            print("Quit")
            self.last_input = "Q"
        return self.last_input