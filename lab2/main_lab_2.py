import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.patches as mpatches
from tkinter import messagebox as mb
import matplotlib.pyplot as plt
import math
import tkinter
from tkinter import *


class Application():
    def __init__(self, window):
        self.t1 = [50., 50.]
        self.t2 = [35., 45.]
        self.t3 = [50., 40.]
        self.x_lim = [0, 100]
        self.y_lim = [0, 100]

        self.first_t1 = [50., 50.]
        self.first_t2 = [35., 45.]
        self.first_t3 = [50., 40.]
        self.first_arc_center = [50., 45]

        self.old_t1 = [[50., 50.]]
        self.old_t2 = [[35., 45.]]
        self.old_t3 = [[50., 40.]]
        self.arc_center = [50., 45]

        self.frame = tkinter.Frame(window)
        tkinter.Button(self.frame, text="Исходное изображение", width=40, font="Arial 18", command=self.go_first).pack(side=TOP)
        tkinter.Button(self.frame, text="Сдвиг", width=10, font="Arial 18", command=self.show_shift_dialog_window).pack(side=TOP)
        tkinter.Button(self.frame, text="Масштабирование", width=35, font="Arial 18",command=self.show_scaling_dialog_window).pack(side=TOP)
        tkinter.Button(self.frame, text="Поворот", width=15, font="Arial 18", command=self.show_rotate_dialog_window).pack(side=LEFT)
        tkinter.Button(self.frame, text="Отмена", width=10, font="Arial 18", command=self.cancel_act).pack(side=RIGHT)

        fig = Figure()
        self.ax = fig.add_subplot(111)
        self.ax = fig.add_subplot(111)
        # self.line, = self.ax.plot(range(10))
        self.ax.set_xlim(self.x_lim[0], self.x_lim[1])
        self.ax.set_ylim(self.y_lim[0], self.y_lim[1])
        self.ellipse = list()
        self.a = 5#self.t1[1] - self.t3[1]
        self.b = 5
        self.x1 = np.linspace(0, 5, 10000)
        for x in self.x1:
            self.ellipse.append([x, -math.sqrt((1 - (x ** 2 / self.a ** 2)) * self.b ** 2)])

        self.x2 = np.linspace(5, 0, 10000)
        for x in self.x2:
            self.ellipse.append([x, math.sqrt((1 - (x ** 2 / self.a ** 2)) * self.b ** 2)])


        for i in self.ellipse:
            i[0] += self.arc_center[0]
            i[1] += self.arc_center[1]
        self.old_ellipse = [self.ellipse.copy()]
        self.first_ellipse = self.ellipse.copy()

        self.draw_figure()
        self.canvas = FigureCanvasTkAgg(fig, master=window)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        self.frame.pack()


    def rewrite_old(self):
        self.old_t1.append(self.t1.copy())
        self.old_t2.append(self.t2.copy())
        self.old_t3.append(self.t3.copy())
        self.old_ellipse.append(self.ellipse.copy())


    def cancel_act(self):
        if len(self.old_t1) <= 1:
            self.show_error_cancel_message()
            return
        self.t1 = self.old_t1.pop()
        self.t2 = self.old_t2.pop()
        self.t3 = self.old_t3.pop()
        self.ellipse = self.old_ellipse.pop()
        self.ax.clear()
        self.draw_figure()
        self.canvas.draw()

    def show_error_cancel_message(self):
        a = tkinter.Toplevel()
        a.title("Ошибка")
        a.geometry('1000x50')
        a.resizable(False, False)
        tkinter.Label(a, text="Нет доступных операций для отмены", font="Arial 18").pack()


    def is_digit(self, x, is_float):
        point_counter = 0
        if (len(x) == 0):
            return False
        for i in range(len(x)):
            if x[i] == '-' and i != 0:
                return False
            elif x[i] == '-' and i == 0:
                continue
            elif x[i] == '.':
                point_counter += 1
                if point_counter > is_float:
                    return False
                if i == 0 or i == len(x) - 1:
                    return False
            else:
                if x[i] < '0' or x[i] > '9':
                    return False
        return True

    def do_rotate(self, xc, yc, angle, a):
        self.ax.clear()
        if (self.is_digit(xc.get(), True) and self.is_digit(yc.get(), True) and self.is_digit(angle.get(), True)):
            self.rewrite_old()
            self.rotate([float(xc.get()), float(yc.get())], float(angle.get()))
            self.draw_figure()
            self.canvas.draw()
            a.destroy()
            a.update()
        else:
            mb.showerror("Ошибка", "Все числа должны быть введены корректно")


    def show_rotate_dialog_window(self):
        a = tkinter.Toplevel()
        a.title("Параметры операции")
        a.geometry('650x300')
        a.resizable(False, False)
        tkinter.Label(a, text="Угол поворота", font="Arial 18").pack()
        angle = tkinter.Entry(a, width=20, font="Arial 18")
        angle.pack()

        tkinter.Label(a, text="Коорднаты центра поворота", font="Arial 18").pack()
        tkinter.Label(a, text="X", font="Arial 18").pack()
        xc = tkinter.Entry(a, width=20, font="Arial 18")
        xc.pack()
        tkinter.Label(a, text="Y", font="Arial 18").pack()
        yc = tkinter.Entry(a, width=20, font="Arial 18")
        yc.pack()
        tkinter.Button(a, text="Применить", font="Arial 18", command= lambda: self.do_rotate(xc, yc, angle, a)).pack()

    def go_first(self):
        self.ax.clear()
        print(type(self.t1))
        self.rewrite_old()
        self.t1 = self.first_t1.copy()
        self.t2 = self.first_t2.copy()
        self.t3 = self.first_t3.copy()
        self.ellipse = self.first_ellipse.copy()
        self.draw_figure()
        self.canvas.draw()


    def do_scaling(self, kx, ky, xc, yc, a):
        self.ax.clear()
        if (self.is_digit(xc.get(), True) and self.is_digit(yc.get(), True) and
                self.is_digit(kx.get(), True) and self.is_digit(ky.get(), True)):
            self.rewrite_old()
            self.scaling_figure(float(kx.get()), float(ky.get()), float(xc.get()), float(yc.get()))
            self.draw_figure()
            self.canvas.draw()
            a.destroy()
            a.update()
        else:
            mb.showerror("Ошибка", "Все числа должны быть введены корректно")


    def show_scaling_dialog_window(self):
        a = tkinter.Toplevel()
        a.title("Параметры операции")
        a.geometry('750x400')
        a.resizable(False, False)

        tkinter.Label(a, text="Коэфициенты масштабирования", font="Arial 18").pack()
        tkinter.Label(a, text="По оси x", font="Arial 18").pack()
        kx = tkinter.Entry(a, width=20, font="Arial 18")
        kx.pack()
        tkinter.Label(a, text="По оси y", font="Arial 18").pack()
        ky = tkinter.Entry(a, width=20, font="Arial 18")
        ky.pack()

        tkinter.Label(a, text="Коорднаты центра масштабирования", font="Arial 18").pack()
        tkinter.Label(a, text="X", font="Arial 18").pack()
        xc = tkinter.Entry(a, width=20, font="Arial 18")
        xc.pack()
        tkinter.Label(a, text="Y", font="Arial 18").pack()
        yc = tkinter.Entry(a, width=20, font="Arial 18")
        yc.pack()
        tkinter.Button(a, text="Применить", font="Arial 18", command= lambda: self.do_scaling(kx, ky, xc, yc, a)).pack()

    def do_shift(self, x_shift, y_shift, a):
        self.ax.clear()
        if (self.is_digit(x_shift.get(), False) and self.is_digit(y_shift.get(), False)):
            self.rewrite_old()
            self.shift_figure(int(x_shift.get()), int(y_shift.get()))
            self.draw_figure()
            self.canvas.draw()
            a.destroy()
            a.update()
        else:
            mb.showerror("Ошибка", "Все числа должны быть введены корректно")


    def show_shift_dialog_window(self):
        a = tkinter.Toplevel()
        a.title("Параметры операции")
        a.geometry('650x200')
        a.resizable(False, False)
        tkinter.Label(a, text="Сдвиг по оси х(целое)", font="Arial 18").pack()
        x_shift = tkinter.Entry(a, width=20, font="Arial 18")
        x_shift.pack()

        tkinter.Label(a, text="Сдвиг по оси y(целое)", font="Arial 18").pack()
        y_shift = tkinter.Entry(a, width=20, font="Arial 18")
        y_shift.pack()
        tkinter.Button(a, text="Применить", font="Arial 18", command= lambda: self.do_shift(x_shift, y_shift, a)).pack()

    def annotte_point(self, point_to_annotate, t1, t2):
        s = "(" + str(round(point_to_annotate[0], 2)) + "," + str(round(point_to_annotate[1], 2)) + ")"
        if point_to_annotate[0] <= t1[0] and point_to_annotate[0] <= t2[0]:
            self.ax.annotate(s, point_to_annotate, [point_to_annotate[0] - 1, point_to_annotate[1]], horizontalalignment='right')
        elif point_to_annotate[0] >= t1[0] and point_to_annotate[0] >= t2[0]:
            self.ax.annotate(s, point_to_annotate, [point_to_annotate[0] + 1, point_to_annotate[1]], horizontalalignment='left')
        elif point_to_annotate[1] <= t1[1] and point_to_annotate[1] <= t2[1]:
            self.ax.annotate(s, point_to_annotate, [point_to_annotate[0], point_to_annotate[1] - 2], verticalalignment='top')
        else:
            self.ax.annotate(s, point_to_annotate, [point_to_annotate[0], point_to_annotate[1] + 2], verticalalignment='bottom')


    def draw_annotate_upper(self):
        x, y = self.t2[0], self.t2[1]
        s = "(" + str(round(x, 2)) + "," + str(round(y, 2)) + ")"
        if (x <= self.t3[0] and x <= self.t1[0]):
                self.ax.annotate(s, self.t2, [x - 2, y], horizontalalignment='right')
        elif (x >= self.t3[0] and x >= self.t1[0]):
            self.ax.annotate(s, self.t2, [x + 2, y], horizontalalignment='left')
            # draw right
        elif (y <= self.t3[1] and y <= self.t1[1]):
            self.ax.annotate(s, self.t2, [x, y - 2], verticalalignment='top')
            # draw bottom
        # draw top
        else:
            self.ax.annotate(s, self.t2, [x, y + 2], verticalalignment='bottom')



    def draw_help_annotate(self, original, copy):
        x, y = original[0], original[1]
        x1, y1 = copy[0], copy[1]
        s = "(" + str(round(x, 2)) + "," + str(round(y, 2)) + ")"

        if (x < x1 and x < self.t2[0]):
            if y < self.t2[1]:
                 # left up
                 self.ax.annotate(s, [x, y], [x - 2, y + 2], horizontalalignment='right', verticalalignment='bottom')
            else:
                self.ax.annotate(s, [x, y], [x - 2, y - 2], horizontalalignment='right', verticalalignment='top')
             # left down

        elif (x > x1 and x > self.t2[0]):
            if y < self.t2[1]:
                self.ax.annotate(s, [x, y], [x + 2, y + 2], horizontalalignment='left', verticalalignment='bottom')
                # right up
            else:
                self.ax.annotate(s, [x, y], [x + 2, y - 2], horizontalalignment='left', verticalalignment='top')
                # right down
        elif (y < y1 and y < self.t2[1]):
            if x < self.t2[0]:
                self.ax.annotate(s, [x, y], [x + 2, y - 2], horizontalalignment='left', verticalalignment='top')
                # right down
            else:
                self.ax.annotate(s, [x, y], [x - 2, y - 2], horizontalalignment='right', verticalalignment='top') # left down
        else:
            if x < self.t2[0]:
                self.ax.annotate(s, [x, y], [x + 2, y + 2], horizontalalignment='left', verticalalignment='bottom') # right up
            else:
                self.ax.annotate(s, [x, y], [x - 2, y + 2], horizontalalignment='right', verticalalignment='bottom')# left up


    def draw_annotate(self):
        self.draw_annotate_upper()
        self.draw_help_annotate(self.t1, self.t3)
        self.draw_help_annotate(self.t3, self.t1)

    def draw_triangle(self):
        X = np.array([self.t1, self.t2, self.t3])
        Y = ['red', 'red', 'red']
        self.ax.scatter(X[:, 0], X[:, 1], s=20, color=Y[:])
        g = plt.Polygon(X[:3, :], color='k', hatch='/')
        g.set_facecolor('w')
        self.ax.add_artist(g)
        self.draw_annotate()

    def draw_ellipse(self):
        X = np.array(self.ellipse)
        g = plt.Polygon(X[:len(X), :], color='k', hatch='/')
        g.set_facecolor('w')
        self.ax.add_artist(g)


    def draw_figure(self):
        self.draw_triangle()
        self.draw_ellipse()
        self.ax.set_xlim(self.x_lim[0], self.x_lim[1])
        self.ax.set_ylim(self.y_lim[0], self.y_lim[1])

    def rotate_point(self, old, center, angle):
        angle = math.radians(angle)
        return [center[0] + (old[0] - center[0]) * math.cos(angle) + (old[1] - center[1]) * math.sin(angle),
                center[1] - (old[0] - center[0]) * math.sin(angle) + (old[1] - center[1]) * math.cos(angle)]

    def rotate(self, center, angle):
        self.t1 = self.rotate_point(self.t1, center, angle)
        self.t2 = self.rotate_point(self.t2, center, angle)
        self.t3 = self.rotate_point(self.t3, center, angle)
        for i, t in enumerate(self.ellipse):
            self.ellipse[i] = self.rotate_point(t, center, angle)
        self.arc_center = self.rotate_point(self.arc_center, center, angle)

    def shift_point(self, point, x_shift, y_shift):
        return [point[0] + x_shift, point[1] + y_shift]

    def shift_figure(self, x_shift, y_shift):
        self.t1 = self.shift_point(self.t1, x_shift, y_shift)
        self.t2 = self.shift_point(self.t2, x_shift, y_shift)
        self.t3 = self.shift_point(self.t3, x_shift, y_shift)
        self.ellipse = [self.shift_point(t, x_shift, y_shift) for t in self.ellipse]

    def scaling_point(self, old, kx, ky, center):
        return [(kx * old[0] + (1 - kx) * center[0]), ky * old[1] + (1 - ky) * center[1]]

    def scaling_figure(self, kx, ky, x_center, y_center):
        self.t1 = self.scaling_point(self.t1, kx, ky, [x_center, y_center])
        self.t2 = self.scaling_point(self.t2, kx, ky, [x_center, y_center])
        self.t3 = self.scaling_point(self.t3, kx, ky, [x_center, y_center])
        self.arc_center = self.scaling_point(self.arc_center, kx, ky, [x_center, y_center])
        for i, t in enumerate(self.ellipse):
            self.ellipse[i] = self.scaling_point(t, kx, ky, [x_center, y_center])

window= tkinter.Tk()
window.geometry('850x1000')
window.title("Lab2 Prokhorova")
window.resizable(False, False)
app = Application(window)
window.mainloop()
