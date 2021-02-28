import os


class DataWriter:
    def __init__(self, timestamp):
        self.filename = os.path.join(
            "/home/pi/SASelfDrivingCar/data/logs", "%d" % timestamp + ".txt"
        )

    def write(self, timestamp, distances, steering):
        with open(self.filename, "a+") as f:
            f.write("%d " % timestamp)
            for distance in distances:
                f.write("%f " % distance)
            if steering == "W":
                f.write("0")
            elif steering == "A":
                f.write("1")
            elif steering == "S":
                f.write("2")
            elif steering == "D":
                f.write("3")
            else:
                f.write("-1")
            f.write("\n")
