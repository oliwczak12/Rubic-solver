from PIL import ImageTk, Image, ImageStat
from Colors import cropGrid, colorArrayToImg, apply_filters, findClosestSettings, saturation
import math
import globals

def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5


mouse_x = 0
mouse_y = 0
cursor = "arrow"
last_mouse_pos = (0, 0)
mouse_last_clic_pos = (0, 0)
grid_corner = ""


def motion(event):
    global mouse_x
    global mouse_y
    global last_mouse_pos
    global cursor
    global grid_corner
    grid = globals.canvas.grid
    mouse_x = event.x
    mouse_y = event.y
    x, y = mouse_x, mouse_y

    if globals.stage == "cam":
        if mouse_x >= int(grid.grid_x) and mouse_x <= (int(grid.grid_x) + grid.cell_size * 3) and mouse_y >= int(grid.grid_y) and mouse_y <= (int(grid.grid_y) + grid.cell_size * 3):
            if mouse_x >= grid.grid_x and mouse_x <= grid.grid_x + 10 and mouse_y >= grid.grid_y and mouse_y <= grid.grid_y + 10:
                cursor = "size_nw_se"
                if not mouse_pressed:
                    grid_corner = "Left-top"
            elif mouse_x >= (grid.grid_x + 3 * grid.cell_size) - 10 and mouse_x <= (grid.grid_x + 3 * grid.cell_size) and mouse_y >= grid.grid_y and mouse_y <= grid.grid_y + 10:
                cursor = "size_ne_sw"
                if not mouse_pressed:
                    grid_corner = "Right-top"
            elif mouse_x >= grid.grid_x and mouse_x <= grid.grid_x + 10 and mouse_y >= (grid.grid_y + 3 * grid.cell_size) - 10 and mouse_y <= (grid.grid_y + 3 * grid.cell_size):
                cursor = "size_ne_sw"
                if not mouse_pressed:
                    grid_corner = "Left-bottom"
            elif (
                mouse_x >= (grid.grid_x + 3 * grid.cell_size) - 10
                and mouse_x <= (grid.grid_x + 3 * grid.cell_size)
                and mouse_y >= (grid.grid_y + 3 * grid.cell_size) - 10
                and mouse_y <= (grid.grid_y + 3 * grid.cell_size)
            ):
                cursor = "size_nw_se"
                if not mouse_pressed:
                    grid_corner = "Right-bottom"
            elif not ((cursor == "size_nw_se" and mouse_pressed) or (cursor == "size_ne_sw" and mouse_pressed)):
                cursor = "fleur"
        else:
            if not mouse_pressed:
                cursor = "arrow"

        if cursor == "fleur" and grid.grid_clicked:
            grid.grid_resized = True
            grid.grid_x += x - last_mouse_pos[0]
            grid.grid_y += y - last_mouse_pos[1]

        if (cursor == "size_nw_se" or cursor == "size_ne_sw") and grid.grid_clicked:
            grid.grid_resized = True

            if grid_corner == "Right-bottom":
                scale = distance(grid.grid_x, grid.grid_y, x, y) / distance(grid.grid_x, grid.grid_y, mouse_last_clic_pos[0], mouse_last_clic_pos[1])
                grid.cell_size = grid.cell_size_before_resize * scale

            if grid_corner == "Left-bottom":
                scale = distance(grid.grid_x + (grid.cell_size_before_resize * 3), grid.grid_y, x, y) / distance(
                    grid.grid_x + (grid.cell_size_before_resize * 3), grid.grid_y, mouse_last_clic_pos[0], mouse_last_clic_pos[1]
                )
                grid.cell_size = grid.cell_size_before_resize * scale
                grid.grid_x = mouse_last_clic_pos[0] + (grid.cell_size_before_resize * 3) - (grid.cell_size * 3)

            if grid_corner == "Left-top":
                scale = distance(grid.grid_x + (grid.cell_size_before_resize * 3), grid.grid_y + (grid.cell_size_before_resize * 3), x, y) / distance(
                    grid.grid_x + (grid.cell_size_before_resize * 3), grid.grid_y + (grid.cell_size_before_resize * 3), mouse_last_clic_pos[0], mouse_last_clic_pos[1]
                )
                grid.cell_size = grid.cell_size_before_resize * (scale)
                grid.grid_x = mouse_last_clic_pos[0] + (grid.cell_size_before_resize * 3) - (grid.cell_size * 3)
                grid.grid_y = mouse_last_clic_pos[1] + (grid.cell_size_before_resize * 3) - (grid.cell_size * 3)

            if grid_corner == "Right-top":
                scale = distance(grid.grid_x, grid.grid_y + (grid.cell_size_before_resize * 3), x, y) / distance(
                    grid.grid_x, grid.grid_y + (grid.cell_size_before_resize * 3), mouse_last_clic_pos[0], mouse_last_clic_pos[1]
                )
                grid.cell_size = grid.cell_size_before_resize * (scale)
                grid.grid_y = mouse_last_clic_pos[1] + (grid.cell_size_before_resize * 3) - (grid.cell_size * 3)
    globals.window.config(cursor=cursor)
    last_mouse_pos = (x, y)


mouse_pressed = False


def on_mouse_press(event):
    global last_mouse_pos
    global mouse_pressed
    global mouse_last_clic_pos
    global cursor
    grid = globals.canvas.grid

    mouse_x = event.x
    mouse_y = event.y
    # print(f"Kliknięto w punkcie: ({event.x}, {event.y})")

    if globals.stage == "cam":
        if mouse_x >= int(grid.grid_x) and mouse_x <= (int(grid.grid_x) + grid.cell_size * 3) and mouse_y >= int(grid.grid_y) and mouse_y <= (int(grid.grid_y) + grid.cell_size * 3):
            grid.grid_clicked = True

        if cursor == "size_nw_se" or cursor == "size_ne_sw":
            grid.cell_size_before_resize = grid.cell_size

        if grid.grid_clicked:
            globals.history.addToUndo(grid)

    last_mouse_pos = (event.x, event.y)
    mouse_last_clic_pos = (event.x, event.y)
    mouse_pressed = True
    globals.mouse1Pressed = True


def on_mouse_release(event):
    global mouse_pressed
    grid = globals.canvas.grid
    # print(f"Przycisk myszy zwolniony na pozycji: ({event.x}, {event.y})")

    grid.grid_clicked = False
    mouse_pressed = False
    globals.mouse1Pressed = False


def on_key_press(event):
    if event.char == " ":
        if globals.screen.freezeFrame:
            globals.screen.freezeFrame = False
        else:
            globals.screen.freezeFrame = True


def undo(event):
    grid = globals.canvas.grid

    last_state = globals.history.undo(grid)
    if last_state:
        last_state["grid_clicked"] = False
        grid.__dict__ = last_state


def redo(event):
    grid = globals.canvas.grid

    next_state = globals.history.redo(grid)
    if next_state:
        next_state["grid_clicked"] = False
        grid.__dict__ = next_state


def brightness(pil_img):
    stat = ImageStat.Stat(pil_img)
    r, g, b = stat.mean
    return math.sqrt(0.241 * (r**2) + 0.691 * (g**2) + 0.068 * (b**2))


def save_button_clicked():
    # print(brightness(Image.fromarray(globals.screen.lastFrame)))
    if not globals.colors_set:
        findClosestSettings(globals.color_list["red"], globals.canvas.grid)
        globals.colors_set = True
    globals.cube.faces[globals.cube.active_face] = cropGrid(apply_filters(Image.fromarray(globals.screen.lastFrame), globals.s1.get(), globals.s2.get()), globals.canvas.grid)
    # globals.cube.faces[globals.cube.active_face] = cropGrid(saturation(Image.fromarray(globals.screen.lastFrame), globals.s3.get()), globals.canvas.grid)
    print(f'"{globals.cube.active_face}":{globals.cube.faces[globals.cube.active_face]},')
    globals.cube.udpateFace(globals.cube.active_face, ImageTk.PhotoImage(colorArrayToImg(globals.cube.faces[globals.cube.active_face])))
    if globals.cube.face_counter < len(globals.cube.faces_names) - 1:
        globals.cube.face_counter += 1
    else:
        globals.cube.face_counter = 0
    globals.cube.active_face = globals.cube.faces_names[globals.cube.face_counter]
    globals.cube.faceActivation(globals.cube.active_face)
    turn = {"up": "Up", "bottom": "Down x2", "right": "Up Right", "back": "Right", "left": "Right", "front": "Red front Yellow on top"}

    
    globals.text.set(turn[globals.cube.active_face])


def next_button_clicked():
    if globals.stage == "cam":
        globals.stage = "cubeConfig"
    elif globals.stage == "cubeConfig":
        globals.stage = "quit"
    globals.canvas.colorSwich.destroy()
    globals.s1.destroy()
    globals.s2.destroy()
    globals.s3.destroy()
    for mesh in globals.cube.cubeMesh.face_meshes.values():
        mesh.destroy()
    globals.save_button.destroy()
    globals.next_button.destroy()
    globals.cube.convertToDefinition()
