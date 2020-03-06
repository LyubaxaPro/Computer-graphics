import math
from tkinter import *
import tkinter
from tkinter.messagebox import *
import matplotlib
import matplotlib.lines as lines
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import matplotlib.pyplot as plt


matplotlib.use('TkAgg')


class DrawApp():
    def __init__(self, appliction):

        self.app = appliction
        if len(self.app.set_1) < 3 or len(self.app.set_2) < 3:
            showwarning('Ошибка', "Недостаточно точек!")
            return

        print(self.app.set_1)

        result = self.app.calc(self.app.set_1, self.app.set_2)
        if result is None:
            showwarning('Ошибка', "Окружностей не найдено!")
            return

        else:

            root = Tk()
            root.title("Поле точек")
            root.geometry('790x1000')
            root.wm_geometry("+%d+%d" % (650, 10))

            x_min = min(self.app.circle1[0], self.app.circle2[0]) - max(self.app.rad1, self.app.rad2)*2
            x_max = max(self.app.circle1[0], self.app.circle2[0]) + max(self.app.rad1, self.app.rad2)*2

            y_min = min(self.app.circle1[1], self.app.circle2[1]) - max(self.app.rad1, self.app.rad2)*2
            y_max = max(self.app.circle1[1], self.app.circle2[1]) + max(self.app.rad1, self.app.rad2)*2

            self.x_lim = [min(x_min, y_min), max(x_max, y_max)]
            self.y_lim = [min(x_min, y_min), max(x_max, y_max)]

            self.frame = tkinter.Frame(root)
            fig = Figure()
            self.ax = fig.add_subplot(111)
            self.ax.set_xlim(self.x_lim[0], self.x_lim[1])
            self.ax.set_ylim(self.y_lim[0], self.y_lim[1])

            self.canvas = FigureCanvasTkAgg(fig, master=root)
            self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
            self.tx = Text(root, width=700, height=10, font='Arial 15')
            self.tx.pack()
            self.frame.pack()

            self.draw_figure()
            root.mainloop()

    def draw_cicrle(self, center, rad, color):
        c = matplotlib.patches.Ellipse(center, 2 * rad, 2 * rad, color=color, fill=False)
        c.set_facecolor('w')
        self.ax.add_artist(c)

    def draw_line(self, p1, p2, color='black'):
        l = lines.Line2D(p1, p2, color=color, linewidth=0.1)
        self.ax.add_artist(l)

    def draw_polygon(self, points, colors):
        self.ax.scatter(points[:, 0], points[:, 1], s=50, color=colors[:])
        g = plt.Polygon(points[:4, :], color='blue', hatch='/', fill=False)
        g.set_facecolor('w')
        self.ax.add_artist(g)

    def draw_point(self, point, color):
        self.ax.scatter(point[0], point[1], s=50, color=color)

    def get_aligment(self, point, center):
        horizontal, vertical = 'center', 'center'
        if (point[0] - center[0]) > 0:
            horizontal = 'left'
        elif (point[0] - center[0]) < 0:
            horizontal = 'right'

        if (point[1] - center[1]) > 0:
            vertical = 'bottom'
        elif (point[1] - center[1]) < 0:
            vertical = 'top'
        return horizontal, vertical


    def get_text(self, point):
        return "({},{})".format(round(point[0], 2), round(point[1], 2))

    def annotate_circle_point(self, point, center):
        annotate_point = [
            point[0] + (point[0] - center[0]) / 5,
            point[1] + (point[1] - center[1]) / 5
        ]
        horizontal, vertical = self.get_aligment(point, center)
        self.ax.annotate(self.get_text(point), point, annotate_point, verticalalignment=vertical, horizontalalignment=horizontal)

    def annotate_center_points(self):
        diff = [
            (self.app.circle1[0] - self.app.circle2[0]),
            (self.app.circle1[1] - self.app.circle2[1])
        ]
        norm = math.sqrt(diff[0]**2 + diff[1]**2)
        shift = 0.1
        diff[0], diff[1] = diff[0] / norm * shift, diff[1] / norm * shift
        horizontal_1, vertical_1 = self.get_aligment(self.app.circle1, self.app.circle2)
        horizontal_2, vertical_2 = self.get_aligment(self.app.circle2, self.app.circle1)

        self.ax.annotate(self.get_text(self.app.circle1), self.app.circle1,
                         [self.app.circle1[0] + diff[0], self.app.circle1[1] + diff[1]],
                         verticalalignment=vertical_1, horizontalalignment=horizontal_1)
        self.ax.annotate(self.get_text(self.app.circle2), self.app.circle2,
                         [self.app.circle2[0] - diff[0], self.app.circle2[1] - diff[1]],
                         verticalalignment=vertical_2, horizontalalignment=horizontal_2)

    def annotate_intersec_point(self):
        if ((self.app.tangent_points1[0][1]  > self.app.tangent_points2[0][1] and self.app.tangent_points1[1][1] > self.app.tangent_points2[0][1]
        and self.app.tangent_points1[0][1]  > self.app.tangent_points2[1][1] and self.app.tangent_points1[1][1] > self.app.tangent_points2[1][1]) or
            (self.app.tangent_points2[0][1] > self.app.tangent_points1[0][1] and self.app.tangent_points2[1][1] > self.app.tangent_points1[0][1]
              and self.app.tangent_points2[0][1] > self.app.tangent_points1[1][1] and self.app.tangent_points2[1][1] > self.app.tangent_points1[1][1])):
            self.ax.annotate(self.get_text(self.app.intersec_point), self.app.intersec_point,
                             [self.app.intersec_point[0] + 1, self.app.intersec_point[1]],
                             horizontalalignment='right')

        elif ((self.app.tangent_points1[0][0] < self.app.tangent_points2[0][0] and self.app.tangent_points1[1][0] < self.app.tangent_points2[0][0] and
               self.app.tangent_points1[0][0] < self.app.tangent_points2[1][0] and self.app.tangent_points1[1][0] < self.app.tangent_points2[1][0]) or
              (self.app.tangent_points2[0][0] < self.app.tangent_points1[0][0] and self.app.tangent_points2[1][0] < self.app.tangent_points1[0][0] and
               self.app.tangent_points2[0][0] < self.app.tangent_points1[1][0] and self.app.tangent_points2[1][0] < self.app.tangent_points1[1][0])):
            self.ax.annotate(self.get_text(self.app.intersec_point), self.app.intersec_point,
                             [self.app.intersec_point[0], self.app.intersec_point[1] + 1],
                             verticalalignment='bottom')
        else:
            self.ax.annotate(self.get_text(self.app.intersec_point), self.app.intersec_point,
                         [self.app.intersec_point[0]+1, self.app.intersec_point[1]],
                         verticalalignment='center_baseline', horizontalalignment='center')

    def print_answ(self):
        self.tx.delete('1.0', END)
        self.tx.insert(1.0, "Окружности найдены.\nМинимальная разность площадей: {0:.3f}\n"
                                      "Окружность 1:\n  Радиус {1:.2f}, координаты центра ({2:.2f}, {3:.2f}) \n"
                                      "Построена на точках с номерами: {4:d}, {5:d} {6:d}\n"
                                      "Окружность 2:\n Радиус {7:.2f}, координаты центра ({8:.2f}, {9:.2f}) \n"
                                      "Построена на точках с номерами: {10:d}, {11:d}, {12:d}\n"
                                      "Точка пересечения касательных ({13:.2f}, {14:.2f})"
                       .format(self.app.min_square, self.app.rad1, self.app.circle1[0], self.app.circle1[1],
                               self.app.set_1.index(self.app.t11) + 1,
                               self.app.set_1.index(self.app.t12) + 1, self.app.set_1.index(self.app.t13) + 1,
                               self.app.rad2, self.app.circle2[0], self.app.circle2[1],
                               self.app.set_2.index(self.app.t21) + 1,
                               self.app.set_2.index(self.app.t22) + 1, self.app.set_2.index(self.app.t23) + 1,
                               self.app.intersec_point[0], self.app.intersec_point[1]))


    def draw_figure(self):
        self.ax.clear()

        # касательные
        # self.draw_line([self.app.tangent_points1[0][0], self.app.tangent_points1[1][0]], [self.app.tangent_points1[0][1], self.app.tangent_points1[1][1]])
        # self.draw_line([self.app.tangent_points2[0][0], self.app.tangent_points2[1][0]], [self.app.tangent_points2[0][1], self.app.tangent_points2[1][1]])
        #

        self.draw_cicrle(self.app.circle1, self.app.rad1, 'r')
        self.draw_cicrle(self.app.circle2, self.app.rad2, 'g')

        self.draw_polygon(
            points=np.array([self.app.circle1,  self.app.tangent_points1[0], self.app.intersec_point, self.app.tangent_points2[0]]),
            colors=['red', 'black', 'black', 'black']
        )
        self.draw_polygon(
            points=np.array([self.app.circle2, self.app.tangent_points1[1], self.app.intersec_point, self.app.tangent_points2[1]]),
            colors=['green', 'black', 'black', 'black']
        )

        for point in self.app.get_points_on_circle(True):
            self.draw_point(point, 'red')
            self.annotate_circle_point(point, self.app.circle1)

        for point in self.app.get_points_on_circle(False):
            self.draw_point(point, 'green')
            self.annotate_circle_point(point, self.app.circle2)

        self.annotate_center_points()
        self.annotate_intersec_point()


        self.draw_line(self.x_lim, [0, 0])
        self.draw_line([0, 0], self.y_lim)

        self.ax.set_xlim(self.x_lim[0], self.x_lim[1])
        self.ax.set_ylim(self.y_lim[0], self.y_lim[1])
        self.canvas.draw()
        self.print_answ()


# a.calc()


