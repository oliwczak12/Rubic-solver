import subprocess
import sys
import pkg_resources  

def install_requirements():
    try:
        with open('requirements.txt', 'r') as file:
            required_packages = file.readlines()
        installed_packages = {pkg.key for pkg in pkg_resources.working_set}
        missing_packages = [pkg.strip() for pkg in required_packages if pkg.split('==')[0] not in installed_packages]

        if missing_packages:
            print(f"Installing missing packages: {', '.join(missing_packages)}")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing_packages])
        else:
            print("All required packages are already installed.")
    except Exception as e:
        print(f"Error installing requirements: {e}")
        sys.exit(1)

install_requirements()


import cv2
import tkinter as tk


import globals
from Screen import Screen


globals.init()
window = globals.window
canvas = globals.canvas
#grid = globals.grid

p = [(21,22),(11,12)]


# Inicjalizacja głównego okna


# Funkcja obsługująca zamykanie okna
def on_closing():
    # Zwolnienie zasobów kamery i zamknięcie okna
    if cap.isOpened():
        cap.release()  # Zwolnienie kamery

    window.destroy()  # Zamykanie okna tkinter


# Ustawienie źródła kamery (0 to domyślna kamera)
cap = globals.cap
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
# Etykieta, na której będzie wyświetlany obraz
canvas.pack(fill="both", expand=True)
# label.pack(fill="both", expand=True)
# label.place(relx=0.0, rely=0.0)



globals.screen.update_frame()


# Obsługa zdarzenia zamknięcia okna
window.protocol("WM_DELETE_WINDOW", on_closing)

# Start głównej pętli aplikacji
window.mainloop()
