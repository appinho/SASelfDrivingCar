from steering import *
import keyboard

while True:
    sleep_time = 0.060
    init()
    try:
        if keyboard.is_pressed("w"):
            print("W")
            forward(sleep_time)
        elif keyboard.is_pressed("a"):
            print("A")
            turn_left(sleep_time)
        elif keyboard.is_pressed("s"):
            print("S")
            reverse(sleep_time)
        elif keyboard.is_pressed("d"):
            print("D")
            turn_right(sleep_time)
        elif keyboard.is_pressed("p"):
            print("P")
            stop(sleep_time)
        elif keyboard.is_pressed("q"):
            stop(sleep_time)
            print("Quit")
            break
        else:
            pass
    except:
        print("Done")
        break
