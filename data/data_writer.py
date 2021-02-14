import os

class DataWriter():
    def __init__(self, timestamp):
        self.filename = os.path.join("/home/pi/SASelfDrivingCar/data/logs", "%d" % timestamp + ".txt")

    def write(self, timestamp, distances, steering):
        with open(self.filename, 'a+') as f:
            f.write("%d " % timestamp)
            for distance in distances:
                f.write("%f " % distance)
            f.write("%s " % steering)
            f.write("\n")