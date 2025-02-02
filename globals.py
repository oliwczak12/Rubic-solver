import cv2
import tkinter as tk
from Grid import Grid
from History import History
import events
from PIL import ImageTk, Image
from CanvasWithGrid import CanvasWithGrid
from Cube import Cube
from Screen import Screen
from TextBox import TextBox


def init():
    global cap
    global grid
    global window
    global canvas
    global history
    global stage
    global cells_crops
    global s1, s2, s3
    global window_width
    global window_height
    global img_container
    global cube
    global screen
    global color_list
    global face_color
    global colors_set
    global text
    global save_button
    global next_button
    global text_box

    history = History()
    cap = cv2.VideoCapture(0)
    window = tk.Tk()
    window_width = 1920
    window_height = 1080
    window.title("Podgląd z kamery")
    window.geometry(f"{window_width}x{window_height}")
    # window.resizable()
    window.state("zoomed")

    canvas = CanvasWithGrid(window, bg="pink")
    img = ImageTk.PhotoImage(Image.open("img/test.jpg"))
    img_container = canvas.create_image(0, 0, anchor="nw", image=img)
    grid = Grid()

    save_button = tk.Button(
        window,
        text="Save",
        command=events.save_button_clicked,
        activebackground="blue",
        activeforeground="white",
        anchor="center",
        bd=3,
        bg="lightgray",
        cursor="hand2",
        disabledforeground="gray",
        fg="black",
        font=("Arial", 12),
        height=2,
        highlightbackground="black",
        highlightcolor="green",
        highlightthickness=2,
        justify="center",
        overrelief="raised",
        padx=10,
        pady=5,
        width=15,
        wraplength=100,
    )
    next_button = tk.Button(
        window,
        text="next",
        command=events.next_button_clicked,
        activebackground="blue",
        activeforeground="white",
        anchor="center",
        bd=3,
        bg="lightgray",
        cursor="hand2",
        disabledforeground="gray",
        fg="black",
        font=("Arial", 12),
        height=2,
        highlightbackground="black",
        highlightcolor="green",
        highlightthickness=2,
        justify="center",
        overrelief="raised",
        padx=10,
        pady=5,
        width=15,
        wraplength=100,
    )

    save_button.place(x=1500, y=600)
    next_button.place(x=300, y=600)

    color_list = {"red": [255, 0, 0], "green": [0, 255, 0], "blue": [0, 0, 255], "yellow": [255, 255, 0], "orange": [255, 140, 0], "white": [255, 255, 255]}

    face_color = {"front": "red", "back": "orange", "left": "blue", "right": "green", "up": "yellow", "bottom": "white"}

    colors_set = False

    cube = Cube()
    cube.createCubeMesh()

    window.bind("<ButtonPress>", events.on_mouse_press)  # Wciśnięcie przycisku myszy
    window.bind("<ButtonRelease>", events.on_mouse_release)

    window.bind("<Motion>", events.motion)
    window.bind("<Key>", events.on_key_press)
    window.bind("<Control-z>", events.undo)
    window.bind("<Control-y>", events.redo)

    stage = "cam"
    w, h = 3, 3
    cells_crops = [[0 for x in range(w)] for y in range(h)]

    # freezeFrame = False
    # lastFrame = None
    label_frame = tk.Frame(window, width=300, height=30, bg="white")
    label_frame.pack_propagate(0)

    text = tk.StringVar()
    text.set("Red front Yellow on top")
    text_box = tk.Label(
        window,
        textvariable=text,
        anchor=tk.CENTER,
        height=1,
        width=30,
        bd=3,
        font=("Arial", 16, "bold"),
        fg="black",
        padx=0,
        pady=0,
        justify=tk.CENTER,
        relief=tk.RAISED,
    )
    text_box.pack()
    window.update()
    
    text_box.place(x=window_width // 2 - (text_box.winfo_width()//2), y=100)
    #label_frame.place(x=window_width // 2 - 150, y=100)
    
    s1 = tk.Scale(canvas, from_=-50, to=100, orient="horizontal")
    s2 = tk.Scale(canvas, from_=-50, to=150, orient="horizontal")
    s3 = tk.Scale(canvas, from_=1, to=3, resolution=0.1, orient="horizontal")
    s1.place(x=window_width // 2, y=window_height - 150)
    s2.place(x=window_width // 2, y=window_height - 200)
    s3.place(x=window_width // 2 + 100, y=window_height - 200)

    screen = Screen()
