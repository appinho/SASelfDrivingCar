import numpy as np
from localization.maps import MAP_X, MAP_Y


class Landmark:
    def __init__(self, i, x, y, o):
        self.i = i
        self.x = x
        self.y = y
        self.o = o

    def show(self):
        print(
            "Landmark %d at %f,%f with o=%f" % (self.i, self.x, self.y, self.o)
        )

    def line_x_rectangle(self, x_min=0, y_min=0, x_max=MAP_X, y_max=MAP_Y):
        a = np.tan(self.o)
        b = self.y - a * self.x
        # Intersections of f(x) = ax + b with the rectangle. (x, y, axis)
        p1, p2 = (
            (x_min, a * x_min + b, "x"),
            (x_max, a * x_max + b, "x"),
        )
        p3, p4 = ((y_min - b) / a, y_min, "y"), ((y_max - b) / a, y_max, "y")
        # Python sorts them using the first key
        p1, p2, p3, p4 = sorted([p1, p2, p3, p4])

        # Check if there is an intersection, returns the points otherwise
        if p1[2] == p2[2]:
            return None
        return p2[:2], p3[:2]

    def get_min_distance2(self):
        points = self.line_x_rectangle()
        if points is None:
            return 100.0
        dx0 = points[0][0] - self.x
        dy0 = points[0][1] - self.y
        dx1 = points[1][0] - self.x
        dy1 = points[1][1] - self.y
        d0 = np.sqrt(dx0 * dx0 + dy0 * dy0)
        d1 = np.sqrt(dx1 * dx1 + dy1 * dy1)
        d = min(d0, d1)
        # print(d)
        return d
