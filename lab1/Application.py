import math


class Application():
    def __init__(self):
        # Example 1
        # self.set_1 = list()
        # self.set_1.append((-1, 0))
        # self.set_1.append((1, 0))
        # self.set_1.append((0, -1))
        #
        # self.set_2 = list()
        # self.set_2.append((4, 0))
        # self.set_2.append((6, 0))
        # self.set_2.append((5, -1))
        # Example 2
        # self.set_1 = list()
        # self.set_1.append((-1, -1))
        # self.set_1.append((1, -1))
        # self.set_1.append((0, -2))
        #
        # self.set_2 = list()
        # self.set_2.append((4, 1))
        # self.set_2.append((6, 1))
        # self.set_2.append((5, 0))
        # Example 3
        # self.set_1 = list()
        # self.set_1.append((-1, -1))
        # self.set_1.append((1, -1))
        # self.set_1.append((0, -2))
        #
        # self.set_2 = list()
        # self.set_2.append((1, 3))
        # self.set_2.append((3, 3))
        # self.set_2.append((2, 4))
        # Example 4
        # self.set_1 = list()
        # self.set_1.append((-1, -1))
        # self.set_1.append((1, -1))
        # self.set_1.append((0, -2))
        #
        # self.set_2 = list()
        # self.set_2.append((-1, 3))
        # self.set_2.append((0, 4))
        # self.set_2.append((1, 3))
        # self.set_2.append((0, 2))


        self.set_1 = list()
        self.set_2 = list()

        self.circle1 = None
        self.circle2 = None
        self.rad1 = None
        self.rad2 = None
        self.tangent_points1 = None
        self.tangent_points2 = None
        self.intersec_point = None

        self.t11=None
        self.t12=None
        self.t13=None
        self.t21=None
        self.t22=None
        self.t23=None

        self.EPS = 0.01

    def is_double(self, point, point2):
        EPS = 0.0001
        if math.fabs(point[0] - point2[0]) < EPS and math.fabs(point[1] - point2[1]) < EPS:
            return True
        return False

    def add_point(self, x, y,  set_number):
        curr_set = self.set_1 if set_number == 1 else self.set_2
        for point in curr_set:
            if self.is_double([x, y], point):
                return False
        curr_set.append([x, y])
        return True

    def change_point(self, point_number, x, y, set_number):
        curr_set = self.set_1 if set_number == 1 else self.set_2
        if len(curr_set) < point_number:
            return False
        for point in curr_set:
            if self.is_double([x, y], point):
                return -2
        curr_set[point_number - 1] = [x, y]
        return True

    def delete_point(self, point_number, set_number):
        curr_set = self.set_1 if set_number == 1 else self.set_2
        if len(curr_set) < point_number:
            return False
        del curr_set[point_number - 1]
        return  True

    def delete_all(self, set_number):
        curr_set = self.set_1 if set_number == 1 else self.set_2
        curr_set.clear()

    def find_area(self, circle_c, t1, t2, intersec):
        a = self.distance_between_points(circle_c, t1)
        b = self.distance_between_points(circle_c, t2)
        c = self.distance_between_points(intersec, t1)
        d = self.distance_between_points(intersec, t2)

        p = (a + b + c + d) / 2
        return math.sqrt((p-a)*(p-b)*(p - c)*(p - d))

    def find_line_intersection(self, line1, line2):
        if abs(line1[0]* line2[1] - line2[0]*line1[1]) < 0.00001:
            print("Lines do not have intersection")
            return
        else:
            x = -1 * ((line1[2]*line2[1] - line2[2]*line1[1])
                      /(line1[0]*line2[1] - line2[0]*line1[1]))
            y = -1 * ((line1[0]*line2[2] - line2[0]*line1[2])/
                      (line1[0]*line2[1]-line2[0]*line1[1]))
            return [x, y]

    def intersec_circle_and_line(self, x, y, r, A, B, C):
        need_swap = math.fabs(B) < self.EPS
        if need_swap:
            x, y = y, x
            A, B = B, A
        a = A**2 + B**2
        b = 2*A*C + 2*A*B*y - 2*B**2*x
        c = C**2 + 2*B*C*y - B**2*(r**2 - x**2 - y**2)
        EPS = 0.0001
        d = b**2 - 4*a*c if math.fabs(b**2 - 4*a*c) > EPS else 0
        solve_x = (-b + math.sqrt(d)) / (2*a)

        if need_swap:
            return -(A*solve_x + C) / B, solve_x
        return solve_x, -(A*solve_x + C) / B

    def get_tangent_coefficients(self, circ1_c, circ2_c, d1, d2):
        circ2_shifted = (circ2_c[0] - circ1_c[0], circ2_c[1] - circ1_c[1])
        dd = d2 - d1
        qq = circ2_shifted[0]**2 + circ2_shifted[1]**2
        ff = math.sqrt(qq - dd**2)
        a = (dd * circ2_shifted[0] + circ2_shifted[1] * ff) / qq
        b = (dd * circ2_shifted[1] - circ2_shifted[0] * ff) / qq

        c = d1 - a*circ1_c[0] - b*circ1_c[1]
        return a, b, c

    def tangent_coefficients(self, circ1_c, r1, circ2_c, r2):
        a1, b1, c1 = self.get_tangent_coefficients(circ1_c, circ2_c, r1, r2 * (-1))
        a2, b2, c2 = self.get_tangent_coefficients(circ1_c, circ2_c, r1 * (-1), r2)
        return [[a1, b1, c1], [a2, b2, c2]]

    def distance_between_points(self, p1, p2):
        dis = math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
        return dis

    def find_circle(self, p1, p2, p3):

        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]
        x3, y3 = p3[0], p3[1]
        if x1 == x2 == x3:  # три точки лежат на одной прямой
            return None
        if x2 == x1:  # случай, когда одна хорда вертикальная, ее коэф = int
            x2, x3 = x3, x2
            y2, y3 = y3, y2
        elif x2 == x3:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        ma = (y2 - y1) / (x2 - x1)  # наклонный коэф 1-ой хорды  p1p2
        mb = (y3 - y2) / (x3 - x2)  # накл коэф 2-ой хорды  p2p3
        if ma != mb:  # прямые не совпадают
            x_centre = (ma * mb * (y1 - y3) + mb * (x1 + x2) - ma * (x2 + x3)) / (2 * (mb - ma))
            if ma == 0:
                y_centre = (-1 / mb) * (x_centre - (x2 + x3) / 2) + ((y2 + y3) / 2)
            else:
                y_centre = (-1 / ma) * (x_centre - (x1 + x2) / 2) + ((y1 + y2) / 2)
            radius = self.distance_between_points([x_centre, y_centre], [x1, y1])
            return [[x_centre, y_centre], radius]
        else:
            return None


    def is_point_on_circle(self, point, center, radius):
        return math.fabs((center[0] - point[0])**2 + (center[1] - point[1])**2 - radius**2) < self.EPS


    def get_points_on_circle(self, is_first):
        circle = self.circle1 if is_first else self.circle2
        rad = self.rad1 if is_first else self.rad2

        for point in (self.set_1 if is_first else self.set_2):
            if self.is_point_on_circle(point, circle, rad):
                yield point


    def calc(self, set1, set2):

        self.set_1 = set1.copy()
        self.set_2 = set2.copy()
        print(self.set_1)
        print(self.set_2)
        min_square = None
        for i in range(len(self.set_1) - 2):  # первая связка-точка
            for j in range(i + 1, len(self.set_1) - 1):  # вторая связка-точка
                for k in range(j + 1, len(self.set_1)):  # третья связка-точка
                    res = self.find_circle(self.set_1[i], self.set_1[j], self.set_1[k])
                    if res is None:
                        continue
                    else:
                        centre_1 = res[0]
                        rad_1 = res[1]

                    for l in range(len(self.set_2) - 2):  # первая связка-точка
                        for m in range(l + 1, len(self.set_2) - 1):  # вторая связка-точка
                            for n in range(m + 1, len(self.set_2)):  # третья связка-точка
                                res = self.find_circle(self.set_2[l], self.set_2[m], self.set_2[n])
                                if res is None:
                                    continue
                                else:
                                    centre_2 = res[0]
                                    rad_2 = res[1]

                                look_dis = self.distance_between_points(centre_2, centre_1)
                                if look_dis <= rad_1 + rad_2:
                                    continue

                                coefficients = self.tangent_coefficients(centre_1, rad_1, centre_2, rad_2)
                                line1 = list()
                                line2 = list()
                                t1_1 = self.intersec_circle_and_line(centre_1[0], centre_1[1], rad_1, coefficients[0][0], coefficients[0][1], coefficients[0][2])
                                t2_1 = self.intersec_circle_and_line(centre_2[0], centre_2[1], rad_2, coefficients[0][0], coefficients[0][1], coefficients[0][2])
                                t1_2 = self.intersec_circle_and_line(centre_1[0], centre_1[1], rad_1, coefficients[1][0], coefficients[1][1], coefficients[1][2])
                                t2_2 = self.intersec_circle_and_line(centre_2[0], centre_2[1], rad_2, coefficients[1][0], coefficients[1][1], coefficients[1][2])
                                line1.append(t1_1)
                                line1.append(t2_1)
                                line2.append(t1_2)
                                line2.append(t2_2)

                                point_intersec = self.find_line_intersection(coefficients[0], coefficients[1])
                                s1 = self.find_area(centre_1, t1_1, t1_2, point_intersec)
                                s2 = self.find_area(centre_2, t2_1, t2_2, point_intersec)

                                dif_s = abs(s2 - s1)

                                if (min_square == None or dif_s < min_square):
                                    self.circle1 = centre_1
                                    self.rad1 = rad_1
                                    self.rad2 = rad_2
                                    self.circle2 = centre_2
                                    self.tangent_points1 = line1.copy()
                                    self.tangent_points2 = line2.copy()
                                    self.min_square = dif_s
                                    self.intersec_point = point_intersec
                                    self.t11=self.set_1[i]
                                    self.t12=self.set_1[j]
                                    self.t13=self.set_1[k]
                                    self.t21=self.set_2[l]
                                    self.t22=self.set_2[m]
                                    self.t23=self.set_2[n]
                                    min_square = dif_s


                                print("-"*60)

                                print("Минимальная разность площадей: {0:.3f}\n"
                                      "Окружность 1: ее радиус {1:.2f}, координаты центра ({2:.2f}, {3:.2f}) \n"
                                      "Построена на точках ({4:.2f}, {5:.2f}); ({6:.2f}, {7:.2f}); ({8:.2f}, {9:.2f})\n"
                                      "Окружность 2: ее радиус {10:.2f}, координаты центра ({11:.2f}, {12:.2f}) \n"
                                      "Построена на точках ({13:.2f}, {14:.2f}); ({15:.2f}, {16:.2f}); ({17:.2f}, {18:.2f})\n"
                                      "Точка пересечения касательных ({19:.2f}, {20:.2f})"
                                      .format(dif_s, rad_1, centre_1[0], centre_1[1], self.set_1[i][0],
                                              self.set_1[i][1],
                                              self.set_1[j][0], self.set_1[j][1], self.set_1[k][0], self.set_1[k][1],
                                              rad_2, centre_2[0], centre_2[1], self.set_2[l][0], self.set_2[l][1],
                                              self.set_2[m][0], self.set_2[m][1], self.set_2[n][0], self.set_2[n][1],
                                              point_intersec[0], point_intersec[1]))

        return min_square
