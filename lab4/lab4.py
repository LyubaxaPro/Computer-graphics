from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPen, QPainter, QColor, QBrush, QImage, QPixmap, QRgba64
from PyQt5.QtCore import Qt
from math import sqrt, pi, cos, sin
import time
from tkinter import Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = QtWidgets.QGraphicsScene(0, 0, 511, 511)
        self.mainview.setScene(self.scene)
        self.image = QImage(511, 511, QImage.Format_ARGB32_Premultiplied)
        self.pen = QPen()
        self.color_line = QColor(Qt.black)
        self.color_bground = QColor(Qt.white)
        self.draw_once.clicked.connect(lambda: draw_once(self))
        self.clean_all.clicked.connect(lambda: clear_all(self))
        self.btn_bground.clicked.connect(lambda: get_color_bground(self))
        self.btn_line.clicked.connect(lambda: get_color_line(self))
        self.draw_centr.clicked.connect(lambda: draw_centr(self))
        self.time_cmp.clicked.connect(lambda: check_time(self))
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.what)
        layout.addWidget(self.other)
        self.setLayout(layout)
        self.circle.setChecked(True)
        self.canon.setChecked(True)


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def circle_canon(win, cx, cy, r, draw):
    for x in range(0, r + 1, 1):
        y = round(sqrt(r ** 2 - x ** 2))

        if draw:
            win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())

    for y in range(0, r + 1, 1):
        x = round(sqrt(r ** 2 - y ** 2))

        if draw:
            win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())


def circle_param(win, cx, cy, r, draw):
    l = round(pi * r / 2 )  # длина четврети окружности
    for i in range(0, l + 1, 1):
        if r != 0:
            x = round(r * cos(i / r))
            y = round(r * sin(i / r))
        else:
            x = 0
            y = 0

        if draw:
            win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())


def circle_brez(win, cx, cy, r, draw):
    x = 0   # задание начальных значений
    y = r
    d = 2 - 2 * r   # значение D(x,y)  при (0,R)
    while y >= 0:

        if draw:
            # высвечивание текущего пиксела
            win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())

        if d < 0:  # пиксель лежит внутри окружности
            buf = 2 * d + 2 * y - 1
            x += 1

            if buf <= 0:  # горизонтальный шаг
                d = d + 2 * x + 1
            else:  # диагональный шаг
                y -= 1
                d = d + 2 * x - 2 * y + 2

            continue

        if d > 0:  # пиксель лежит вне окружности
            buf = 2 * d - 2 * x - 1
            y -= 1

            if buf > 0:  # вертикальный шаг
                d = d - 2 * y + 1
            else:  # диагональный шаг
                x += 1
                d = d + 2 * x - 2 * y + 2

            continue

        if d == 0.0:  # пиксель лежит на окружности
            x += 1   # диагональный шаг
            y -= 1
            d = d + 2 * x - 2 * y + 2


def circle_middle(win, cx, cy, r, draw):
    x = 0  # начальные значения
    y = r
    p = 5 / 4 - r  # (x + 1)^2 + (y - 1/2)^2 - r^2
    while True:
        if draw:
            win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())

            win.image.setPixel(cx - y, cy + x, win.pen.color().rgb())
            win.image.setPixel(cx + y, cy - x, win.pen.color().rgb())
            win.image.setPixel(cx - y, cy - x, win.pen.color().rgb())
            win.image.setPixel(cx + y, cy + x, win.pen.color().rgb())

        x += 1

        if p < 0:  # средняя точка внутри окружности, ближе верхний пиксел, горизонтальный шаг
            p += 2 * x + 1
        else:   # средняя точка вне окружности, ближе диагональный пиксел, диагональный шаг
            p += 2 * x - 2 * y + 5
            y -= 1

        if x > y:
            break


def ellips_canon(win, cx, cy, a, b, draw):
    for x in range(0, a + 1, 1):
        if (a == 0):
            y = round(b)
        else:
            y = round(b * sqrt(1.0 - x ** 2 /(a ** 2)))

        if draw:
            win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())

    for y in range(0, b + 1, 1):
        if (b == 0):
            x = round(a)
        else:
            x = round(a * sqrt(1.0 - y ** 2 / (b ** 2)))

        if draw:
            win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())




def ellips_param(win, cx, cy, a, b, draw):
    m = max(a, b)
    l = round(pi * m / 2)
    for i in range(0, l + 1, 1):
        if m == 0:
            x = 0
            y = 0
        else:
            x = round(a * cos(i / m))
            y = round(b * sin(i / m))

        if draw:
            win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())


def ellips_brez(win, cx, cy, a, b, draw):
    x = 0  # начальные значения
    y = b
    a = a ** 2
    d = round(b * b / 2 - a * b * 2 + a / 2)
    b = b ** 2
    while y >= 0:
        if draw:
            win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())
        if d < 0:  # пиксель лежит внутри эллипса
            buf = 2 * d + 2 * a * y - a
            x += 1
            if buf <= 0:  # горизотальный шаг
                d = d + 2 * b * x + b
            else:  # диагональный шаг
                y -= 1
                d = d + 2 * b * x - 2 * a * y + a + b

            continue

        if d > 0:  # пиксель лежит вне эллипса
            buf = 2 * d - 2 * b * x - b
            y -= 1

            if buf > 0:  # вертикальный шаг
                d = d - 2 * y * a + a
            else:  # диагональный шаг
                x += 1
                d = d + 2 * x * b - 2 * y * a + a + b

            continue

        if d == 0.0:  # пиксель лежит на окружности
            x += 1  # диагональный шаг
            y -= 1
            d = d + 2 * x * b - 2 * y * a + a + b


def ellips_middle(win, cx, cy, a, b, draw):
    x = 0   # начальные положения
    y = b
    p = b * b - a * a * b + 0.25 * a * a   # начальное значение параметра принятия решения в области tg<1
    while 2 * (b ** 2) * x < 2 * a * a * y:  # пока тангенс угла наклона меньше 1
        if draw:
            win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())

        x += 1

        if p < 0:  # средняя точка внутри эллипса, ближе верхний пиксел, горизонтальный шаг
            p += 2 * b * b * x + b * b
        else:   # средняя точка вне эллипса, ближе диагональный пиксел, диагональный шаг
            y -= 1
            p += 2 * b * b * x - 2 * a * a * y + b * b

    p = b * b * (x + 0.5) * (x + 0.5) + a * a * (y - 1) * (y - 1) - a * a * b * b
    # начальное значение параметра принятия решения в области tg>1 в точке (х + 0.5, y - 1) полседнего положения

    while y >= 0:

        if draw:
            win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())
            win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())

        y -= 1

        if p > 0:
            p -= 2 * a * a * y + a * a
        else:
            x += 1
            p += 2 * b * b * x - 2 * a * a * y + a * a

# Рисование одной фигуры
def draw_once(win):
    is_standart = False
    x = win.centr_x.value()
    y = win.centr_y.value()

    if win.circle.isChecked():
        r = win.rad.value()

        if win.canon.isChecked():
            circle_canon(win, x, y, r, True)
        if win.param.isChecked():
            circle_param(win, x, y, r, True)
        if win.brez.isChecked():
            circle_brez(win, x, y, r, True)
        if win.middle.isChecked():
            circle_middle(win, x, y, r, True)
        if win.lib.isChecked():
            is_standart = True
            win.scene.addEllipse(x - r, y - r, r * 2, r * 2, win.pen)

    if win.ellips.isChecked():
        a = win.a.value()
        b = win.b.value()

        if win.canon.isChecked():
            ellips_canon(win, x, y, b, a, True)
        if win.param.isChecked():
            ellips_param(win, x, y, b, a, True)
        if win.brez.isChecked():
            ellips_brez(win, x, y, b, a, True)
        if win.middle.isChecked():
            ellips_middle(win, x, y, b, a, True)
        if win.lib.isChecked():
            is_standart = True
            win.scene.addEllipse(x - b, y - a, b * 2, a * 2, win.pen)


    if not is_standart:
        pix = QPixmap(511, 511)
        pix.convertFromImage(win.image)
        win.scene.addPixmap(pix)

# Рисование концентрических окружностей/эллипсов
def draw_centr(win):
    is_standart = False
    x = win.centr_x.value()
    y = win.centr_y.value()
    d = win.step.value()
    c = win.count.value()

    if win.circle.isChecked():
        for i in range(d, d * c + d, d):

            if win.canon.isChecked():
                circle_canon(win, x, y, i, True)
            if win.param.isChecked():
                circle_param(win, x, y, i, True)
            if win.brez.isChecked():
                circle_brez(win, x, y, i, True)
            if win.middle.isChecked():
                circle_middle(win, x, y, i, True)
            if win.lib.isChecked():
                is_standart = True
                win.scene.addEllipse(x - i, y - i, i * 2, i * 2, win.pen)

    if win.ellips.isChecked():
        for i in range(d, d * c + d, d):
            if win.canon.isChecked():
                ellips_canon(win, x, y, i * 2, i, True)
            if win.param.isChecked():
                ellips_param(win, x, y, i * 2, i, True)
            if win.brez.isChecked():
                ellips_brez(win, x, y, i * 2, i, True)
            if win.middle.isChecked():
                ellips_middle(win, x, y, i * 2, i, True)
            if win.lib.isChecked():
                is_standart = True
                win.scene.addEllipse(x - i * 2, y - i, i * 4, i * 2, win.pen)


    if not is_standart:
        pix = QPixmap(511, 511)
        pix.convertFromImage(win.image)
        win.scene.addPixmap(pix)


def get_color_bground(win):
    color = QtWidgets.QColorDialog.getColor(initial=Qt.white, title='Цвет фона',
                                            options=QtWidgets.QColorDialog.DontUseNativeDialog)
    if color.isValid():
        win.color_bground = color
        win.image.fill(color)
        s = QtWidgets.QGraphicsScene(0, 0, 10, 10)
        s.setBackgroundBrush(color)
        win.bground_color.setScene(s)
        win.scene.setBackgroundBrush(color)


def get_color_line(win):
    color = QtWidgets.QColorDialog.getColor(initial=Qt.black, title='Цвет линии',
                                            options=QtWidgets.QColorDialog.DontUseNativeDialog)
    if color.isValid():
        win.color_line = color
        win.pen.setColor(color)
        s = QtWidgets.QGraphicsScene(0, 0, 10, 10)
        s.setBackgroundBrush(color)
        win.line_color.setScene(s)


def clear_all(win):
    win.image.fill(Qt.color0)
    win.scene.clear()

def show_graph_window(title, size, figsize, xlab, ylab, names, rad, times):
    root = Tk()
    root.title(title)
    root.geometry(size)
    fig = Figure(figsize=figsize)
    ax = fig.add_subplot(111)
    ax.set_ylabel(ylab)
    ax.set_xlabel(xlab)
    ax.plot(rad, times[0], label=names[0], color='g')
    ax.plot(rad, times[1], label=names[1], color='r')
    ax.plot(rad, times[2], label=names[2], color='b')
    ax.plot(rad, times[3], label=names[3], color='y')
    ax.grid(True)
    ax.legend()
    canvas = FigureCanvasTkAgg(fig, root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    root.mainloop()

def calc_time_circ(func, window, cx, cy, r):
    count = 20
    start_time = time.perf_counter()
    for i in range(count):
        func(window, cx, cy, r, False)
    stop_time = time.perf_counter()
    return (stop_time - start_time) / count * (10 ** 3)

def calc_time_ellipse(func, window, cx, cy, a, b):
    count = 20
    start_time = time.perf_counter()
    for i in range(count):
        func(window, cx, cy, a, b, False)
    stop_time = time.perf_counter()
    return (stop_time - start_time) / count * (10 ** 3)


def check_time(win):
    cx = 255
    cy = 255

    time_canon = []
    time_param = []
    time_brez = []
    time_mid = []

    if win.circle.isChecked():
        rad = [r for r in range (0, 400, 10)]
        for r in rad:
            time_canon.append(calc_time_circ(circle_canon, win, cx, cy, r))
            time_param.append(calc_time_circ(circle_param, win, cx, cy, r))
            time_brez.append(calc_time_circ(circle_brez, win, cx, cy, r))
            time_mid.append(calc_time_circ(circle_middle, win, cx, cy, r))

        show_graph_window('Зависимость времени работы алгоритмов от радиуса', '650x700', (150, 100), 'Радиус', "Время(мс)", ['Каноническое уравнение',
                    "Параметрическое уравнение", "Алгоритм Брезенхема", "Алгоритм средней точки"], rad, [time_canon, time_param, time_brez, time_mid])

    if win.ellips.isChecked():
        b = [r for r in range (0, 400, 10)]
        for i in b:
            if win.canon.isChecked():
                time_canon.append(calc_time_ellipse(ellips_canon, win, cx, cy, i * 2, i))
                time_param.append(calc_time_ellipse(ellips_param, win, cx, cy, i * 2, i))
                time_brez.append(calc_time_ellipse(ellips_brez, win, cx, cy, i * 2, i ))
                time_mid.append(calc_time_ellipse(ellips_middle, win, cx, cy, i * 2, i))

        show_graph_window('Зависимость времени работы алгоритмов от изменения полуоси', '650x700', (150, 100), 'Полуось', "Время(мс)", ['Каноническое уравнение',
                    "Параметрическое уравнение", "Алгоритм Брезенхема", "Алгоритм средней точки"], b, [time_canon, time_param, time_brez, time_mid])



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
