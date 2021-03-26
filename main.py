from tkinter import *
from tkinter import messagebox as mb
import math


# Visas 2D transformācijas šeit
class Transformation:

    # Pārvieto visus punktus uz norādīto pikseļu skaitu
    @staticmethod
    def move_object(points, tx, ty):

        result = list()
        for x in points:
            result.append((x[0] + tx, x[1] + ty))
        return result

    # Mērogot visus punktus attiecībā pret figuras centru
    @staticmethod
    def scale_object(points, sx, sy):

        central_point = Transformation.get_central_point(points)
        result = list()
        for x in points:
            if (x[0] < central_point[0]):
                res_x = central_point[0] - ((central_point[0] - x[0]) * sx)
            else:
                res_x = central_point[0] + ((x[0] - central_point[0]) * sx)

            if (x[1] < central_point[1]):
                res_y = central_point[1] - ((central_point[1] - x[1]) * sy)
            else:
                res_y = central_point[1] + ((x[1] - central_point[1]) * sy)

            result.append((int(res_x), int(res_y)))

        return result

    # Pagriež visus punktus attiecībā pret norādītem koordinātiem uz norādīto leņķi
    @staticmethod
    def rotate_object(points, rx, ry, angle):
        result = list()
        radians = math.radians(angle)
        for x in points:
            res_x = (rx + (x[0] - rx) * math.cos(radians)) - (x[1] - ry) * math.sin(radians)
            res_y = (x[0] - rx) * math.sin(radians) + (ry + (x[1] - ry) * math.cos(radians))
            result.append((int(res_x), int(res_y)))
        return result

    # Atgriež centrālo punktu
    @staticmethod
    def get_central_point(points):
        x_sum = 0
        y_sum = 0
        point_quantity = len(points)

        for x in points:
            x_sum += int(x[0])
            y_sum += int(x[1])

        return (round(x_sum / point_quantity), round(y_sum / point_quantity))

    # Veic pilnu transformaciju ar punktiem ar paramietriem, kuri doti ká StringVar nevis int
    @staticmethod
    def full_transform_with_var(points, tx_var, ty_var, sx_var, sy_var, rx_var, ry_var, angle_var):
        # tx un ty pēc noklusējuma ir 0
        try:
            tx = int(tx_var.get())
        except ValueError:
            tx = 0

        try:
            ty = int(ty_var.get())
        except ValueError:
            ty = 0

        moved_points = Transformation.move_object(points, tx, ty)

        # sx un sy pēc noklusējuma ir 1
        try:
            sx = float(sx_var.get())
        except ValueError:
            sx = 1

        try:
            sy = float(sy_var.get())
        except ValueError:
            sy = 1

        scaled_points = Transformation.scale_object(moved_points, sx, sy)

        # leņķis pēc noklusējuma ir 0
        try:
            angle = int(angle_var.get())
        except ValueError:
            angle = 0

        # Punkts ap kuru rotes figura pēc noklusējuma ir centralais punkts
        try:
            rx = int(rx_var.get())
            ry = int(ry_var.get())
        except ValueError:
            central_point = Transformation.get_central_point(scaled_points)
            rx = central_point[0]
            ry = central_point[1]

        return Transformation.rotate_object(scaled_points, rx, ry, angle)


# Galvenais ekrāns
class TransformationApp(Tk):
    def __init__(self):
        super().__init__()
        self.title('Proga')
        self.geometry('1280x720')
        self.resizable(False, False)
        self.point_list = list()

        self.top_frame = TopFrame(self)
        self.top_frame.place(relwidth=1, relheight=0.1)

        self.rigth_frame = RightFrame(self)
        self.rigth_frame.place(relwidth=0.3, relheight=0.9, relx=0.7, rely=0.1)

        self.new_plane()

    def get_points(self):
        return self.point_list

    def add_point(self, point):
        self.point_list.append(point)

    def get_plane(self):
        return self.plane

    def new_plane(self):
        self.plane = CartesianPlane(self)
        self.plane.place(relwidth=0.7, relheight=0.9, relx=0, rely=0.1)


# Labais panelis, kurā ir iestatījumu lauki un palaišanas poga
class RightFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='#D9D9D9')

        # Panelis ar nobídes iestátíjumiem
        move_sett_frame = Frame(self, bg='#FFFFFF', borderwidth=15)
        move_sett_frame.pack(padx=5, pady=5, fill=BOTH, expand=True)
        move_label = Label(move_sett_frame, text='Nobīde', font=('Segoe', '16', 'bold'), bg='#FFFFFF')
        move_label.grid(column=0, row=0, columnspan=3, sticky=(W))
        # tx block
        tx_label = Label(move_sett_frame, text='tx = ', font=('Segoe', '14'), bg='#FFFFFF')
        tx_label.grid(column=0, row=1, pady=21, sticky=(W))
        tx_var = StringVar();
        tx_entry = Entry(move_sett_frame, textvariable=tx_var, width=35)
        tx_entry.grid(column=1, row=1, pady=21, padx=10)
        pixel_label1 = Label(move_sett_frame, text='pikseli', font=('Segoe', '14'), bg='#FFFFFF')
        pixel_label1.grid(column=2, row=1, pady=21, padx=10)
        # ty block
        ty_label = Label(move_sett_frame, text='ty = ', font=('Segoe', '14'), bg='#FFFFFF')
        ty_label.grid(column=0, row=2, sticky=(W))
        ty_var = StringVar();
        ty_entry = Entry(move_sett_frame, textvariable=ty_var, width=35)
        ty_entry.grid(column=1, row=2, padx=10)
        pixel_label2 = Label(move_sett_frame, text='pikseli', font=('Segoe', '14'), bg='#FFFFFF')
        pixel_label2.grid(column=2, row=2, padx=10)

        # Panelis ar merogošanas iestátíjumiem
        scale_sett_frame = Frame(self, bg='#FFFFFF', borderwidth=15)
        scale_sett_frame.pack(padx=5, pady=5, fill=BOTH, expand=True)
        scale_label = Label(scale_sett_frame, text='Mērogošana', font=('Segoe', '16', 'bold'), bg='#FFFFFF')
        scale_label.grid(column=0, row=0, columnspan=3, sticky=(W))
        # sx block
        sx_label = Label(scale_sett_frame, text='sx = ', font=('Segoe', '14'), bg='#FFFFFF')
        sx_label.grid(column=0, row=1, pady=21, sticky=(W))
        sx_var = StringVar();
        sx_entry = Entry(scale_sett_frame, textvariable=sx_var, width=35)
        sx_entry.grid(column=1, row=1, pady=21, padx=10)
        scalerate_label1 = Label(scale_sett_frame, text='X', font=('Segoe', '14'), bg='#FFFFFF')
        scalerate_label1.grid(column=2, row=1, pady=21, padx=10)
        # sy block
        sy_label = Label(scale_sett_frame, text='sy = ', font=('Segoe', '14'), bg='#FFFFFF')
        sy_label.grid(column=0, row=2, sticky=(W))
        sy_var = StringVar();
        sy_entry = Entry(scale_sett_frame, textvariable=sy_var, width=35)
        sy_entry.grid(column=1, row=2, padx=10)
        scalerate_label2 = Label(scale_sett_frame, text='X', font=('Segoe', '14'), bg='#FFFFFF')
        scalerate_label2.grid(column=2, row=2, padx=10)

        # Panelis ar pagriešanas iestátíjumiem
        rotate_sett_frame = Frame(self, bg='#FFFFFF', borderwidth=15)
        rotate_sett_frame.pack(padx=5, pady=5, fill=BOTH, expand=True)
        scale_label = Label(rotate_sett_frame, text='Pagriešana', font=('Segoe', '16', 'bold'), bg='#FFFFFF')
        scale_label.grid(column=0, row=0, columnspan=3, sticky=(W))
        # angle block
        angle_label = Label(rotate_sett_frame, text='leņķis =', font=('Segoe', '14'), bg='#FFFFFF')
        angle_label.grid(column=0, row=1, sticky=(W), pady=20)
        angle_var = StringVar();
        angle_entry = Entry(rotate_sett_frame, textvariable=angle_var, width=31)
        angle_entry.grid(column=1, row=1, padx=10, pady=20, sticky=(W))
        degree_label = Label(rotate_sett_frame, text='°', font=('Segoe', '14'), bg='#FFFFFF')
        degree_label.grid(column=2, row=1, pady=20, sticky=(W))
        # rotate point block
        scale_label = Label(rotate_sett_frame, text='Punkts, ap kuru rotēs objekts: ', font=('Segoe', '12', 'bold'),
                            bg='#FFFFFF')
        scale_label.grid(column=0, row=2, columnspan=3, sticky=(W))
        xy_frame = Frame(rotate_sett_frame, bg='#FFFFFF')
        xy_frame.grid(column=0, row=3, columnspan=3, sticky=(W), pady=20)
        rx_label = Label(xy_frame, text='x = ', font=('Segoe', '14'), bg='#FFFFFF')
        rx_label.pack(side=LEFT)
        rx_var = StringVar();
        rx_entry = Entry(xy_frame, textvariable=rx_var)
        rx_entry.pack(side=LEFT, padx=10)
        ry_label = Label(xy_frame, text='y = ', font=('Segoe', '14'), bg='#FFFFFF')
        ry_label.pack(side=LEFT)
        ry_var = StringVar();
        ry_entry = Entry(xy_frame, textvariable=ry_var)
        ry_entry.pack(side=LEFT, padx=10)

        # Galvēna poga, pēc nospiešanas zīmē divas figūras grafikā - pamatojoties uz ievadītajiem punktiem(sarkana)
        # un pamatojoties uz transformētajiem (zaļa)
        start_button = Button(
            self,
            text='Pielietot',
            font=('Segoe', '16', 'bold'),
            fg='#FFFFFF',
            bg='#111B69',
            relief='flat',
            command=lambda: [
                parent.new_plane(),
                parent.get_plane().draw_figure(parent.get_points(), 'red'),
                parent.get_plane().draw_figure(Transformation.full_transform_with_var(
                    parent.get_points(), tx_var, ty_var, sx_var, sy_var, rx_var, ry_var, angle_var
                ), 'green')
            ]
        )
        start_button.pack(padx=5, pady=5, fill=BOTH, expand=True)
        parent.bind('<Return>', lambda e: start_button.invoke())


# Augšējais panelis, satur pogu jaunu punktu pievienošanai figurai un paneļiem ar jau pievienoto punktu koordinātām (max 10)
class TopFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent, bg='#111B69', borderwidth=15)
        self.plus_button = Button(self, text=' + ', command=self.coord_input, font=('Segoe', '16', 'bold'),
                                  relief='flat')
        self.plus_button.grid(column=0, row=0, padx=5)
        self.point_frames_list = list()
        self.parent = parent

    def add_point(self, x, y):
        try:
            int_x = int(x)
            int_y = int(y)
            parent.add_point((int_x, int_y))
        except ValueError:
            mb.showerror("ERROR", "Nav pareizi dati")
            return

        point_frame = PointFrame(self, x, y)

        point_frame.grid(column=len(self.point_frames_list), row=0, padx=2)
        self.point_frames_list.append(point_frame)

        # Ограничение на 10 точек
        if (len(self.point_frames_list) < 10):
            self.plus_button.grid(column=len(self.point_frames_list), row=0, padx=5)

    def shift_frames(self, from_index):
        if (from_index == 0):
            from_index = 1

        for x in range(from_index, len(self.point_frames_list)):
            self.point_frames_list[x].grid(column=x - 1, row=0, padx=2)

    def remove_point(self, point_frame):
        parent.point_list.pop(self.point_frames_list.index(point_frame))
        self.point_frames_list.remove(point_frame)

    def coord_input(self):
        point_input_window = CoordInputWindow(parent=self.parent, top_frame=self)


# Panelis ar punktu koordinatám
class PointFrame(Frame):
    def __init__(self, parent, x, y):
        super().__init__(parent)
        point_coord_label = Label(self, text='(' + x + ' ; ' + y + ')', font=('Segoe', '16', 'bold'), bg='#FFFFFF')
        point_coord_label.grid(column=0, row=0, ipadx=5, ipady=5)

        close_button = Button(
            self,
            text='X',
            font=('Segoe', '16', 'bold'),
            relief='flat',
            fg='#7F0000',
            bg='#FFFFFF',
            command=lambda: [parent.shift_frames(parent.point_frames_list.index(self)),
                             parent.remove_point(self),
                             self.destroy()
                             ]
        )
        close_button.grid(column=1, row=0)


# Papildlogs, lai ievadītu jauna punkta koordinātas
class CoordInputWindow(Toplevel):
    def __init__(self, parent, top_frame):
        super().__init__(parent)
        self.title('Ievadiet koordinātas')
        self.geometry("200x150")
        self.resizable(False, False)

        point_input_frame = Frame(self, bg='#FFFFFF', borderwidth=15)
        point_input_frame.place(relwidth=1, relheight=1, relx=0, rely=0);

        x_label = Label(point_input_frame, text='x = ', font=('Segoe', '14'), bg='#FFFFFF')
        y_label = Label(point_input_frame, text='y = ', font=('Segoe', '14'), bg='#FFFFFF')

        x = StringVar()
        y = StringVar()
        x_entry = Entry(point_input_frame, textvariable=x, width=21)
        y_entry = Entry(point_input_frame, textvariable=y, width=21)

        x_label.grid(column=0, row=0, sticky=(W))
        y_label.grid(column=0, row=1, sticky=(W), pady=20)
        x_entry.grid(column=1, row=0, sticky=(E))
        y_entry.grid(column=1, row=1, sticky=(E), pady=20)

        ok_button = Button(
            point_input_frame,
            text='Ok',
            font=('Segoe', '12', 'bold'),
            width=12,
            fg='#FFFFFF',
            bg='#111B69',
            relief='flat',
            command=lambda: [top_frame.add_point(x.get(), y.get()), self.destroy()]
        )
        ok_button.grid(column=0, row=2, columnspan=2)
        self.bind('<Return>', lambda e: ok_button.invoke())


# Dekarta koordinātu plakne
class CartesianPlane(Canvas):

    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.create_line(0, 324, 896, 324, width=2, arrow=LAST)
        self.create_line(448, 648, 448, 0, width=2, arrow=LAST)

        for i in range(48, 849, 50):
            self.create_line(i, 321, i, 327, width=1)
            if (i != 448):
                self.create_text(i, 340, text=str(i - 448))

        for i in range(24, 625, 50):
            self.create_line(445, i, 451, i, width=1)
            if (i != 324):
                self.create_text(465, i, text=str(324 - i))

    # Metode, figuras zimēšanai
    def draw_figure(self, points, color):
        for i in range(0, len(points)):
            start = CartesianPlane.conv_cartesian_coord(points[i])
            if (i == len(points) - 1):
                finish = CartesianPlane.conv_cartesian_coord(points[0])
            else:
                finish = CartesianPlane.conv_cartesian_coord(points[i + 1])
            self.create_line(start[0], start[1], finish[0], finish[1], fill=color, width=2)

    # Parveido Dekarta koordinates us koordinatiem, kuri dēr attelošanai Canvas'ā
    def conv_cartesian_coord(coordinates):
        conv_x = coordinates[0] + 448
        conv_y = 324 - coordinates[1]
        return (conv_x, conv_y)


# Programmas palaišana
parent = TransformationApp()
parent.mainloop()