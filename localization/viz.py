import matplotlib.pyplot as plt
import matplotlib.patches as patches
from maps import MAP_X, MAP_Y
import numpy as np

EDGE = 50
RES = 200
ARROW = 30
COLORS = ["g", "r", "c", "m", "y"]

def get_color(i):
    j = i % len(COLORS)
    return COLORS[j]

def draw_particle(ax, p, c):
	#x_2 = np.cos(p.o) * ARROW
    #y_2 = np.sin(p.o) * ARROW
    #
    #x_e = x_2
    #y_e = y_2
    x_s = p.x * RES
    y_s = p.y * RES
    ax.plot(x_s, y_s, c)

def draw_landmark(ax, l, c):
    x_s = l.x * RES
    y_s = l.y * RES
    ax.plot(x_s, y_s, c)

def draw(title, particles, i, best_index=-1, save=False, draw=False):

        fig, ax = plt.subplots(1)
        ax.set_xlim([-EDGE * MAP_X, EDGE * MAP_X + RES * MAP_X])
        ax.set_ylim([-EDGE * MAP_Y, EDGE * MAP_Y + RES * MAP_Y])
        rect = patches.Rectangle(
            (0, 0),
            RES * MAP_X,
            RES * MAP_Y,
            linewidth=1,
            edgecolor="k",
            facecolor="none",
        )
        ax.add_patch(rect)

        for p in particles:
            if p.i == best_index:
                continue	
            draw_particle(ax, p, 'c.')
            for l in p.landmarks:
            	draw_landmark(ax, l, 'c.')

        if best_index >= 0:
            p = particles[best_index]
            draw_particle(ax, p, 'gs')
            p.show()
            # x_off = np.cos(p.o) * 5
            # x2 = [p.x * RES, x_off * RES]
            # y2 = [0, MAP_Y * RES]
            for l in p.landmarks:
                x1 = p.x * RES
                x2 = (p.x + np.cos(l.o) * 5) * RES
                y1 = p.y * RES
                y2 = (p.y + np.sin(l.o) * 5) * RES
            	plt.plot([x1, x2], [y1, y2], color='r', marker = 'o')
                draw_landmark(ax, l, 'gs')
                l.show()
            
        plt.title(title)
        if save:
            plt.savefig("./data/loc/" + "{0:0=3d}".format(i))
        elif draw:
            plt.show()
        plt.close('all')