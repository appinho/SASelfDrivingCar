import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw(self, title, best_index=-1, save=False, draw=False):

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

        for p in self.particles:
            if best_index != -1 and p.i != best_index:
                continue
            # p.print()
            x_2 = np.cos(p.o) * ARROW
            y_2 = np.sin(p.o) * ARROW
            x_s = p.x * RES
            y_s = p.y * RES
            x_e = x_2
            y_e = y_2
            c = GET_COLOR(p.i)
            # c = 'k'
            ax.arrow(
                x_s, y_s, x_e, y_e, head_width=10, head_length=10, fc=c, ec=c
            )
        for l in self.landmarks:
            if best_index != -1 and l.i != best_index:
                continue
            c = GET_COLOR(l.i)
            # c = 'k'
            ax.plot(l.x * RES, l.y * RES, c + "o")
        plt.title(title)
        if save:
            plt.savefig("./data/loc/" + "{0:0=3d}".format(self.i))
        elif draw:
            plt.show()