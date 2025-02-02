import globals


class Grid:
    def __init__(self):
        self.grid_resized = False
        self.cell_size = 200
        self.grid_x = int((globals.window_width / 2) - (self.cell_size * 1.5))
        self.grid_y = int((globals.window_height / 2) - (self.cell_size * 1.5))
        self.grid_clicked = False
        self.cell_size_before_resize = 0
        self.x = 0
        self.y = 0
        self.rec_list = []
        self.fill = []
