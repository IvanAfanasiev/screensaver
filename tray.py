from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor

def create_icon():
    size = 64
    pixmap = QPixmap(size, size)
    pixmap.fill(QColor("black"))

    painter = QPainter(pixmap)
    painter.setBrush(QColor("white"))
    painter.setPen(QColor("white"))
    rect_size = 32
    rect_x = (size - rect_size) // 2
    rect_y = (size - rect_size) // 2
    painter.drawRoundedRect(rect_x, rect_y, rect_size, rect_size, 8, 8)
    painter.end()

    return QIcon(pixmap)

def start_tray(app, on_quit_callback=None, on_play_callback=None):
    tray = QSystemTrayIcon()
    tray.setIcon(create_icon()) 
    tray.setToolTip("Screensaver")
    menu = QMenu()

    play_action = QAction("Play", app)
    if on_play_callback:
        play_action.triggered.connect(on_play_callback)
    menu.addAction(play_action)

    quit_action = QAction("Quit", app)
    if on_quit_callback:
        quit_action.triggered.connect(on_quit_callback)
    else:
        quit_action.triggered.connect(app.quit)
    menu.addAction(quit_action)

    tray.setContextMenu(menu)
    tray.show()

    return tray