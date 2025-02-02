from PIL import Image, ImageTk
from drawing import gridDrawRec
from Colors import apply_filters

import cv2
import globals


class Screen:
    def __init__(self):
        self.cap = globals.cap
        self.window = globals.window

        self.canvas = globals.canvas
        self.grid = self.canvas.grid
        self.frame = None
        self.freezeFrame = None
        self.lastFrame = None
        self.cube = globals.cube
        self.img_container = globals.img_container

    def update_frame(self):
        # Przechwycenie klatki z kamery
        if not self.freezeFrame:
            ret, frame = self.cap.read()
            # TODO: sprawdźć czy już nie jest takiej wielkości
            frame = cv2.resize(frame, (1920, 1080))
            if ret:
                self.lastFrame = frame.copy()

        else:
            ret = True

        if ret:
            if self.freezeFrame:
                frame = self.lastFrame.copy()

            
            gridDrawRec(self.canvas, self.grid.grid_x, self.grid.grid_y, self.grid.cell_size, 3, 3)

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            if self.canvas.color_swich:
                img = ImageTk.PhotoImage(apply_filters(Image.fromarray(frame_rgb), globals.s1.get(), globals.s2.get(), globals.s3.get()))
            else:
                img = ImageTk.PhotoImage(Image.fromarray(frame_rgb))


            self.canvas.itemconfig(self.img_container, image=img)
            self.canvas._image_ref = img
            if globals.stage == "cam":
                self.window.after(20, self.update_frame)
            elif globals.stage == "cubeConfig":
                self.cap.release()
                self.cube.cubeConfig()
