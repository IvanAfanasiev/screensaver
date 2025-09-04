import ctypes
import time
import pyautogui
import random
from ctypes import *
from ctypes.wintypes import *
from pynput import mouse, keyboard

user_active = False
user32 = ctypes.windll.user32
user_active = False

def on_move(x, y):
    global user_active
    user_active = True
    return False  # stop listener
def on_key_pressed(key):
    global user_active
    user_active = True
    return False  # stop listener

def main():
    mouse_listener = mouse.Listener(
        on_move=on_move, 
        on_click=lambda *a: on_move(x, y), 
        on_scroll=lambda *a: on_move(x, y)
        )
    mouse_listener.start()
    keyboard_listener = keyboard.Listener(on_press=on_key_pressed)
    keyboard_listener.start()

    #screen size
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    SetCursorPos = ctypes.windll.user32.SetCursorPos

    # start position
    x, y = pyautogui.position()

    # V2 direction
    dir_x, dir_y = random.randint(2, 5), random.randint(3, 5)
    fps = 60

    # mouse movement = the exit trigger
    while not user_active:
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
        time.sleep(0.5 / fps)



if __name__ == "__main__":
    main()