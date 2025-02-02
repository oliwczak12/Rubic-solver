import numpy as np
import math
import globals
from tkinter import Canvas
from PIL import Image, ImageTk
#import kociemba
import twophase.solver  as kociemba


class Cube:
    def __init__(self):
        self.cell_size = 200

        self.cubeMesh = None
        self.cube_mesh_cell_size = 33
        self.pil_blank_img = Image.new("RGB", (3 * self.cube_mesh_cell_size, 3 * self.cube_mesh_cell_size))
        gray_color = (128, 128, 128)
        for x in range(self.pil_blank_img.width):
            for y in range(self.pil_blank_img.height):
                self.pil_blank_img.putpixel((x, y), gray_color)

        self.blank_img = ImageTk.PhotoImage(self.pil_blank_img)
        self.front_img = self.blank_img
        self.back_img = self.blank_img
        self.right_img = self.blank_img
        self.left_img = self.blank_img
        self.up_img = self.blank_img
        self.bottom_img = self.blank_img
        self.faces_names = ["front", "up", "bottom", "right", "back", "left"]
        self.face_counter = 0
        self.active_face = self.faces_names[self.face_counter]
        self.faces = {"front": [[(0, 255, 0), (255, 255, 255), (0, 255, 0)], [(255, 140, 0), (255, 0, 0), (255, 0, 0)], [(255, 255, 255), (255, 0, 0), (255, 255, 0)]],
                      "back": [[(0, 0, 255), (0, 0, 255), (0, 255, 0)], [(255, 140, 0), (255, 140, 0), (255, 140, 0)], [(255, 255, 255), (255, 140, 0), (255, 140, 0)]],
                      "right": [[(255, 255, 255), (255, 255, 0), (255, 140, 0)], [(255, 255, 0), (0, 255, 0), (0, 255, 0)], [(255, 0, 0), (0, 0, 255), (255, 0, 0)]],
                      "left": [[(255, 140, 0), (255, 255, 255), (255, 0, 0)], [(0, 0, 255), (0, 0, 255), (255, 255, 0)], [(0, 0, 255), (0, 0, 255), (0, 255, 0)]],
                      "up": [[(255, 255, 0), (255, 255, 0), (255, 255, 0)], [(0, 255, 0), (255, 255, 0), (0, 255, 0)], [(255, 255, 0), (255, 0, 0), (255, 140, 0)]],
                      "bottom": [[(255, 0, 0), (0, 255, 0), (0, 0, 255)], [(255, 255, 255), (255, 255, 255), (255, 0, 0)], [(255, 255, 255), (255, 255, 255), (0, 0, 255)]]
                      }
        self.faces_imgs = {"right": self.right_img, "bottom": self.bottom_img, "left": self.left_img, "up": self.up_img, "front": self.front_img, "back": self.back_img}
        self.every_color = []

        self.window = globals.window
        self.canvas = globals.canvas

    def createCubeMesh(self):
        self.cubeMesh = CubeMesh(self.faces_imgs, 200, 200, self.cube_mesh_cell_size, self.window)
        # self.test()

    def udpateFace(self, face, img):
        self.faces_imgs[face] = img
        self.cubeMesh.updateFace(face, img)

    def faceActivation(self, face):
        self.cubeMesh.drawBorder(face)

    def cubeConfigRun(self):
        self.window.after(10, self.cubeConfigRun)

    def cubeConfig(self):
        self.canvas.configure(scrollregion=(-self.window.winfo_width() // 2, -self.window.winfo_height() // 2, self.window.winfo_width() // 2, self.window.winfo_height() // 2))
        self.canvas.xview_moveto(0.5)
        self.canvas.yview_moveto(0.5)
        self.canvas.update()
        cubePreview = CubePreview(self.canvas)
        # cubePreview.
        # Bind mouse events
        self.canvas.bind("<Button-1>", cubePreview.start_drag)
        self.canvas.bind("<B1-Motion>", cubePreview.on_drag)
        self.canvas.bind("<ButtonRelease-1>", cubePreview.stop_drag)
        # canvas.bind("<Enter>", cubePreview.colorOutline)
        self.window.update()
        self.cubeConfigRun()

    def convertToDefinition(self):
        face_order = ["up","right","front","bottom","left","back"]
        colors = {(255, 0, 0): "red", (0, 255, 0): "green", (0, 0, 255): "blue", (255, 255, 0): "yellow", (255, 140, 0): "orange", (255, 255, 255): "white"}
        color_list = {(255, 0, 0): "F", (0, 255, 0): "R", (0, 0, 255): "L", (255, 255, 0): "U", (255, 140, 0): "B", (255, 255, 255): "D"}
        definition = ""
        
        for face in face_order:
            for row in self.faces[face]:
                for color in row:
                    definition += color_list[color]
        
        print(definition)
        try:
            solve = kociemba.solve(definition)
            globals.text_box.config(width=len(solve))
            globals.text.set(solve)
            globals.window.update()
            globals.text_box.place(x=globals.window_width // 2 - (globals.text_box.winfo_width()//2), y=100)
            print(solve)
        except:
            print("Niemozliwe ułożenie kolorów")
        
        

class CubeFaceMesh(Canvas):
    def __init__(self, face, face_name, x, y, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.width = kwargs["width"]
        self.cell_size = self.width / 3
        self.create_image(0, 0, anchor="nw", image=face)

        self.create_line(0, self.cell_size, self.width, self.cell_size, width=2)
        self.create_line(0, self.cell_size * 2, self.width, self.cell_size * 2, width=2)
        self.create_line(self.cell_size, 0, self.cell_size, self.width, width=2)
        self.create_line(self.cell_size * 2, 0, self.cell_size * 2, self.width, width=2)
        self.create_rectangle(0, 0, self.width - 1, self.width - 1, width=4)
        self.place(x=x, y=y)
        self.face_name = face_name

        self.info = []
        self.bind("<Enter>", self.showInfo)
        self.bind("<Leave>", self.hideInfo)
        self.bind("<Button-1>", self.select)
    
    def redraw(self):
        self.create_line(0, self.cell_size, self.width, self.cell_size, width=2)
        self.create_line(0, self.cell_size * 2, self.width, self.cell_size * 2, width=2)
        self.create_line(self.cell_size, 0, self.cell_size, self.width, width=2)
        self.create_line(self.cell_size * 2, 0, self.cell_size * 2, self.width, width=2)
        self.create_rectangle(0, 0, self.width - 1, self.width - 1, width=4)

    def drawBorder(self):
        self.create_rectangle(0, 0, self.width - 1, self.width - 1, width=4, outline="cyan")

    def showInfo(self, event):
        self.info.append(self.create_rectangle(0, 0, self.width - 1, self.width - 1, fill="white", outline="white"))
        self.info.append(self.create_text(self.width / 2, self.width / 2, text=self.face_name))

    def hideInfo(self, event):
        for info in self.info:
            self.delete(info)
            
    def select(self,event):
        globals.cube.active_face = self.face_name


class CubeMesh:
    def __init__(self, faces, x, y, cell_size, window):
        self.face_meshes = {"right": None, "bottom": None, "left": None, "up": None, "front": None, "back": None}
        for i, face in enumerate(faces):
            if i <= 3:
                self.face_meshes[face] = CubeFaceMesh(faces[face], face, x + cell_size * 3 * i - i, y, window, bg="red", width=cell_size * 3, height=cell_size * 3, bd=0, highlightthickness=0)
            else:
                self.face_meshes[face] = CubeFaceMesh(
                    faces[face],
                    face,
                    x + cell_size * 9 - 3,
                    y + cell_size * 3 - cell_size * 6 * (i % 4) + (-1 + 2 * (i % 4)),
                    window,
                    bg="red",
                    width=cell_size * 3,
                    height=cell_size * 3,
                    bd=0,
                    highlightthickness=0,
                )

    def updateFace(self, face, img):
        self.face_meshes[face].delete("all")
        self.face_meshes[face].create_image(0, 0, anchor="nw", image=img)
        self.face_meshes[face].redraw()

    def drawBorder(self, face):
        self.face_meshes[face].drawBorder()


class IrregularGrid:
    def __init__(self, canvas, face):
        self.face = face
        self.canvas = canvas
        self.out_line_color = "black"
        self.outline_width = 2
        self.colors = [["pink"] * 3 for _ in range(3)]

    def drawDividedQuadrilateral(self, A, B, C, D):
        top = [self.interpolate(A, B, t) for t in [0, 1 / 3, 2 / 3, 1]]
        right = [self.interpolate(B, C, t) for t in [0, 1 / 3, 2 / 3, 1]]
        bottom = [self.interpolate(D, C, t) for t in [0, 1 / 3, 2 / 3, 1]]
        left = [self.interpolate(A, D, t) for t in [0, 1 / 3, 2 / 3, 1]]
        
        for i in range(3):
            for j in range(3):
                p1 = self.interpolate(left[i], right[i], j / 3)
                p2 = self.interpolate(left[i], right[i], (j + 1) / 3)
                p3 = self.interpolate(left[i + 1], right[i + 1], (j + 1) / 3)
                p4 = self.interpolate(left[i + 1], right[i + 1], j / 3)
                self.canvas.create_polygon(p1, p2, p3, p4, fill=self.colors[i][j], width=self.outline_width, outline=self.out_line_color)

    def interpolate(self, p1, p2, t):
        return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))

    def updateColor(self, row, col, color):
        if 0 <= row < 3 and 0 <= col < 3:
            if type(color) is tuple:
                colorval = "#%02x%02x%02x" % color
                self.colors[row][col] = colorval
            else:
                self.colors[row][col] = color
            
    def rotateColorMatrix(self):
        self.colors=list(zip(*self.colors))[::-1]
        
    def mirrorMatrix(self):
        for c in self.colors:
            c = c.reverse()
             
    def redraw(self):
        self.canvas.delete("all")
        A = (100, 100)
        B = (300, 80)
        C = (250, 250)
        D = (50, 220)
        self.drawDividedQuadrilateral(A, B, C, D)


class CubePreview:
    def __init__(self, canvas):
        self.canvas = canvas

        self.colors = ["red", "blue", "green", "orange", "yellow", "white"]
        self.faces = globals.cube.faces
        # Initialize rotation angles
        self.angleX = 0.5
        self.angleY = 0.5

        # Mouse tracking variables
        self.last_x = 0
        self.last_y = 0
        self.dragging = False
        self.P = np.array(
            [
                [-50, -50, -50],
                [50, -50, -50],
                [50, 50, -50],
                [-50, 50, -50],
                [-50, -50, 50],
                [50, -50, 50],
                [50, 50, 50],
                [-50, 50, 50],
            ]
        )

        self.projection = np.array([[1, 0, 0], [0, 1, 0]])

        self.drawFaces()
        self.colorFaces()
        self.draw()

    def draw(self):
        self.canvas.delete("all")

        rotationX = np.array([[1, 0, 0], [0, math.cos(self.angleX), -math.sin(self.angleX)], [0, math.sin(self.angleX), math.cos(self.angleX)]])

        rotationY = np.array([[math.cos(self.angleY), 0, math.sin(self.angleY)], [0, 1, 0], [-math.sin(self.angleY), 0, math.cos(self.angleY)]])

        P_temp = self.P.copy()
        points_to_draw = []

        for i in range(len(P_temp)):
            rotated = np.dot(rotationY, P_temp[i])
            rotated = np.dot(rotationX, rotated)

            z_distance = 200
            perspective_factor = z_distance / (rotated[2] + z_distance)

            p = np.dot(self.projection, rotated) * perspective_factor
            P_temp[i][0], P_temp[i][1] = p[0], p[1]
            points_to_draw.append((p[0], p[1], rotated[2]))

        faces = [
            (points_to_draw[5], points_to_draw[4], points_to_draw[7], points_to_draw[6], "Back"),
            (points_to_draw[0], points_to_draw[1], points_to_draw[2], points_to_draw[3], "Front"),
            (points_to_draw[4], points_to_draw[0], points_to_draw[3], points_to_draw[7], "Left"),
            (points_to_draw[1], points_to_draw[5], points_to_draw[6], points_to_draw[2], "Right"),
            (points_to_draw[4], points_to_draw[5], points_to_draw[1], points_to_draw[0], "Up"),
            (points_to_draw[3], points_to_draw[2], points_to_draw[6], points_to_draw[7], "Down"),
        ]

        faces.sort(key=lambda x: sum(point[2] for point in x[:4]) / 4, reverse=True)

        face_mapping = {
            "Back": self.face_Back,
            "Front": self.face_Front,
            "Right": self.face_Right,
            "Left": self.face_Left,
            "Up": self.face_Up,
            "Down": self.face_Down,
        }

        for face in faces:
            if face[4] in face_mapping:
                face_mapping[face[4]].drawDividedQuadrilateral(*[corner[:2] for corner in face[:4]])


        if self.dragging:
            globals.window.after(20, self.draw)

    def drawFaces(self):
        self.face_Front = IrregularGrid(self.canvas,"front")
        self.face_Back = IrregularGrid(self.canvas,"back")
        self.face_Right = IrregularGrid(self.canvas,"right")
        self.face_Left = IrregularGrid(self.canvas,"left")
        self.face_Up = IrregularGrid(self.canvas,"up")
        self.face_Down = IrregularGrid(self.canvas,"down")

    def colorFaces(self):
        for i in range(3):
            for j in range(3):
                self.face_Front.updateColor(i, j, self.faces["front"][i][j])
                self.face_Back.updateColor(i, j, self.faces["back"][i][j])
                self.face_Right.updateColor(i, j, self.faces["right"][i][j])
                self.face_Left.updateColor(i, j, self.faces["left"][i][j])
                self.face_Up.updateColor(i, j, self.faces["up"][i][j])
                self.face_Down.updateColor(i, j, self.faces["bottom"][i][j])
        #self.face_Up.mirrorMatrix()
        #self.face_Up.rotateColorMatrix()
        

    def colorOutline(self, event):
        self.faces["front"].out_line_color = "magenta"
        self.faces["front"].outline_width = 4

    def start_drag(self, event):
        self.last_x = event.x
        self.last_y = event.y
        self.dragging = True
        self.draw()

    def on_drag(self, event):
        if self.dragging:
            dx = event.x - self.last_x
            dy = event.y - self.last_y

           
            self.angleY += -dx * 0.01
            self.angleX += dy * 0.01

            self.last_x = event.x
            self.last_y = event.y

    def stop_drag(self, event):
        self.dragging = False
