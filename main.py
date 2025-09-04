import ctypes
import time
import pyautogui
import random
from ctypes import *
from ctypes.wintypes import *

user_active = False
user32 = ctypes.windll.user32

def main():
    #screen size
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    SetCursorPos = ctypes.windll.user32.SetCursorPos

    # start position
    x, y = pyautogui.position()

    # V2 direction
    dir_x, dir_y = random.randint(2, 5), random.randint(3, 5)
    fps = 60

    while True:
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