import ctypes
import time
import pyautogui
import random
from ctypes import *
from ctypes.wintypes import *
from pynput import mouse, keyboard
from PyQt5.QtWidgets import QApplication, QWidget
import sys
import threading

from tray import start_tray


user32 = ctypes.windll.user32
window_visible = False
user_active = False

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("screensaver Black")
window.setStyleSheet("background-color: black;")

def start_animation():
    #screen size
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    SetCursorPos = ctypes.windll.user32.SetCursorPos

    # start position
    x, y = pyautogui.position()

    # V2 direction
    directions = [-5, -4, -3, 3, 4, 5]
    dir_x = random.choice(directions)
    dir_y = random.choice(directions)
    fps = 60
    speed = 2

    # mouse movement = the exit trigger
    while not user_active:
        if user_active:
            return
        
        x += dir_x
        y += dir_y

        if x <= 0:
            x = 0
            dir_x = -dir_x
        elif x >= screen_width - 1:
            x = screen_width - 1
            dir_x = -dir_x

        if y <= 0:
            y = 0
            dir_y = -dir_y
        elif y >= screen_height - 1:
            y = screen_height - 1
            dir_y = -dir_y

        SetCursorPos(x, y)
        time.sleep(1 / fps * speed)

def hide_window():
    global window_visible
    if window_visible:
        window.hide()
        window_visible = False

def show_window():
    global window_visible
    global user_active
    if not window_visible:
        window.showFullScreen()
        user_active = False
        try:
            threading.Thread(target=start_animation, daemon=True).start()
        except:
            hide_window()
            pass
        window_visible = True
        
def on_any_activity():
    global user_active
    user_active = True
    hide_window()

def close():
    app.quit()

def start_listeners():
    mouse_listener = mouse.Listener(
        on_move=on_any_activity,
        on_click=on_any_activity, 
        on_scroll=on_any_activity
        )
    mouse_listener.start()
    keyboard_listener = keyboard.Listener(on_press=on_any_activity)
    keyboard_listener.start()

def main():
    threading.Thread(target=start_listeners, daemon=True).start()

    tray = start_tray(app, on_quit_callback=close, on_play_callback=show_window)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()