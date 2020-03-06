from tkinter.messagebox import *
from tkinter import *

from DrawApp import DrawApp
from Application import Application


class GraphicApp():
    def __init__(self):

        r = Tk()
        r.title("Инструменты")
        r.wm_geometry("+%d+%d" % (10, 10))
        #
        self.app = Application()
        self.scale = 9
        self.dx = 10
        self.dy = 10
        self.redraw_scale = False
        self.redraw_d = False

        self.num_r_lst = 1
        self.num_g_lst = 1

        self.scrollbar1 = Scrollbar(r)
        self.scrollbar2 = Scrollbar(r)
        self.r_lst = Listbox(r, selectmode=SINGLE, height=20, width=30, yscrollcommand=self.scrollbar1.set)
        self.g_lst = Listbox(r, selectmode=SINGLE, height=20, width=30, yscrollcommand=self.scrollbar2.set)
        self.scrollbar1.config(command=self.r_lst.yview)
        self.scrollbar2.config(command=self.g_lst.yview)
        self.lab_f = Label(r, text="Множество красных точек", font="Arial 18")
        self.lab_s = Label(r, text="Множество зелёных точек", font="Arial 18")
        self.lab_shift = Label(r, text="      ", font="Arial 18")
        self.but_add_r = Button(r, text= 'Добавить красную точку', width=40, font="Arial 18", command=lambda: self.show_add_dialog_window(1))
        self.but_add_g = Button(r, text='Добавить зелёную точку', width=40, font="Arial 18", command=lambda: self.show_add_dialog_window(2))
        self.but_del_r = Button(r, text='Удалить красную точку', width=40, font="Arial 18", command=lambda: self.show_del_dialog_window(1))
        self.but_del_g = Button(r, text='Удалить зелёную точку', width=40, font="Arial 18", command=lambda: self.show_del_dialog_window(2))
        self.but_del_all_r = Button(r, text='Удалить все красные точки', width=50, font="Arial 18", command=lambda: self.delete_all(1))
        self.but_del_all_g = Button(r, text='Удалить все зелёные точки', width=50, font="Arial 18", command=lambda: self.delete_all(2))
        self.but_ch_r = Button(r, text='Изменить красную точку', width=40, font="Arial 18", command=lambda: self.show_change_dialog_window(1))
        self.but_ch_g = Button(r, text='Изменить зелёную точку', width=40, font="Arial 18", command=lambda: self.show_change_dialog_window(2))
        self.but_answ = Button(r, text='Решить задачу', width=40, font="Arial 18", command=self.ddd)

        self.r_lst.grid(row=1, column=0, padx=10)
        self.g_lst.grid(row=1, column=2, padx=10)
        self.lab_f.grid(row=0, column=0, padx=5)
        self.lab_s.grid(row=0, column=2, padx=5)
        self.lab_shift.grid(row=0, column=1, padx=5)
        self.but_add_g.grid(row=3, column=2, padx=5, pady=10)
        self.but_add_r.grid(row=3, column=0, padx=5, pady=10)
        self.but_del_r.grid(row=4, column=0, padx=5, pady=10)
        self.but_del_g.grid(row=4, column=2, padx=5, pady=10)
        self.but_del_all_r.grid(row=5, column=0, padx=5, pady=10)
        self.but_del_all_g.grid(row=5, column=2, padx=5, pady=10)
        self.but_ch_r.grid(row=6, column=0, padx=5, pady=10)
        self.but_ch_g.grid(row=6, column=2, padx=5, pady=10)
        self.but_answ.grid(row=7, column=1, padx=5, pady=10)
        #
        # self.x_lim = [0, 100]
        # self.y_lim = [0, 100]
        # # self.cnv = Canvas(root, height=600, width=700, bg='white')
        # # self.tx = Text(root, width=700, height=4, font='Times 12')
        # self.frame = tkinter.Frame(root)
        # fig = Figure()
        # self.ax = fig.add_subplot(111)
        # self.ax = fig.add_subplot(111)
        # # self.line, = self.ax.plot(range(10))
        # self.ax.set_xlim(self.x_lim[0], self.x_lim[1])
        # self.ax.set_ylim(self.y_lim[0], self.y_lim[1])

        # self.cnv.pack()
        # self.tx.pack()

        r.mainloop()

    def ddd(self):
        print(str(self.app.set_2))
        a = DrawApp(self.app)
        print(str(self.app.set_2))


    def str_to_float(self, a):
        if a == '':
            return None
        a = a.split(' ')
        for i in range(len(a)):
            try:
                a[i] = float(a[i])
            except ValueError:
                showwarning('Упс', "Данные введены некорректно")
                return None
        return a

    def str_to_int(self, a):
        if a == '':
            return None
        a = a.split(' ')
        for i in range(len(a)):
            try:
                a[i] = int(a[i])
            except ValueError:
                showwarning('Упс', "Данные введены некорректно")
                return None
        if int(a[0]) <= 0:
            showwarning('Упс', "Данные введены некорректно")
            return None
        return a

    def insert_to_list(self, curr_set, x, y):
        if curr_set == 1:
            p = [self.num_r_lst, x, y]
            self.r_lst.insert(END, p)
            self.num_r_lst += 1
        else:
            p = [self.num_g_lst, x, y]
            self.g_lst.insert(END, p)
            self.num_g_lst += 1

    def show_add_dialog_window(self, curr_set):
        def insert_lst(event):
            p = self.ent_f.get()
            p = self.str_to_float(p)
            if p is None:
                return
            if len(p) > 2 or len(p) < 2:
                showwarning('Упс', "У точки должно быть всего две координаты!")
                return
            if self.app.add_point(p[0], p[1], curr_set):
                self.insert_to_list(curr_set, p[0], p[1])
            self.ent_f.delete(0, END)
            if curr_set == 1:
                print(self.app.set_1)
            else:
                print(self.app.set_2)

        a = Toplevel()
        a.title("Добавить точку")
        a.geometry('650x200')
        a.resizable(False, False)
        Label(a, text="Введите координаты точки\n( через пробел)", font="Arial 18").pack()
        self.ent_f = Entry(a, width=20, font="Arial 18")
        self.ent_f.bind('<Return>', insert_lst)
        self.ent_f.pack()

    def show_del_dialog_window(self, curr_set):

        def delete_lst(event):
            p = self.ent_f.get()
            p = self.str_to_int(p)
            if p is None:
                return
            if len(p) != 1:
                showwarning('Упс', "Введите номер точки корректно!")
                return
            if curr_set == 1 and p[0] > len(self.app.set_1) or curr_set == 2 and p[0] > len(self.app.set_2):
                showwarning('Упс', "Нет точки с таким номером!")
                return
            if self.app.delete_point(p[0], curr_set):
                if (curr_set == 1):
                    self.r_lst.delete(0, END)
                    self.num_r_lst = 1
                    for i in self.app.set_1:
                        self.insert_to_list(curr_set, i[0], i[1])
                else:
                    self.g_lst.delete(0, END)
                    self.num_g_lst = 1
                    for i in self.app.set_2:
                        self.insert_to_list(curr_set, i[0], i[1])

            self.ent_f.delete(0, END)
        a = Toplevel()
        a.title("Удалить точку")
        a.geometry('450x200')
        a.resizable(False, False)
        Label(a, text="Введите номер точки", font="Arial 18").pack()
        self.ent_f = Entry(a, width=10, font="Arial 18")
        self.ent_f.bind('<Return>', delete_lst)
        self.ent_f.pack()

    # def draw(self):
    #
    #     if self.app.set_1 is None or self.app.set_2 is None:
    #         showerror('Ошибка', 'Введите точки в формате х,у')
    #         return
    #     if len(self.app.set_1) < 3 or len(self.app.set_2) < 3:
    #         showerror('Ошибка', 'Недостаточно точек')
    #         return

    def show_change_dialog_window(self, curr_set):
        def change_lst():
            p = self.ent_f.get()
            p = self.str_to_int(p)
            if p is None:
                return
            if len(p) != 1:
                showwarning('Упс', "Введите номер точки корректно!")
                return
            if curr_set == 1 and p[0] > len(self.app.set_1) or curr_set == 2 and p[0] > len(self.app.set_2):
                showwarning('Упс', "Нет точки с таким номером!")
                return
            xy = self.xy_f.get()
            xy = self.str_to_float(xy)
            if xy is None:
                return
            if len(xy) > 2 or len(xy) < 2:
                showwarning('Упс', "У точки должно быть всего две координаты!")
                return
            t = self.app.change_point(p[0], xy[0], xy[1], curr_set)
            if t == -2:
                showwarning('Упс', "Точка с такими координатами уже существует!")
                return
            if t:
                if (curr_set == 1):
                    self.r_lst.delete(0, END)
                    self.num_r_lst = 1
                    for i in self.app.set_1:
                        self.insert_to_list(curr_set, i[0], i[1])
                else:
                    self.g_lst.delete(0, END)
                    self.num_g_lst = 1
                    for i in self.app.set_2:
                        self.insert_to_list(curr_set, i[0], i[1])

            self.ent_f.delete(0, END)
            self.xy_f.delete(0, END)
        a = Toplevel()
        a.title("Изменить координаты точки")
        a.geometry('750x200')
        a.resizable(False, False)
        a1 = Label(a, text="Введите номер точки", font="Arial 18")
        a1.grid(column=0, row=0)
        self.ent_f = Entry(a, width=10, font="Arial 18")
        self.ent_f.grid(column=0, row=1)
        a2 = Label(a, text="Введите новые координаты точки", font="Arial 18")
        a2.grid(column=0, row=2)
        self.xy_f = Entry(a, width=20, font="Arial 18")
        self.xy_f.grid(column=0, row=3)
        b = Button(a, text='Применить', width=40, font="Arial 18", command=change_lst)
        b.grid(column=0, row=4)



    def delete_all(self, curr_set):
        if (curr_set == 1):
            self.r_lst.delete(0, END)
            self.num_r_lst = 1
        else:
            self.g_lst.delete(0, END)
            self.num_g_lst = 1

        self.app.delete_all(curr_set)
