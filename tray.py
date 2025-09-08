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

def start_tray(app, on_quit_callback=None, on_start_callback=None, on_show_settings=None):
    tray = QSystemTrayIcon()
    tray.setIcon(create_icon()) 
    tray.setToolTip("Screensaver")
    menu = QMenu()

    start_action = QAction("Start", app)
    if on_start_callback:
        start_action.triggered.connect(on_start_callback)
    menu.addAction(start_action)

    settings_action = QAction("Settings", app)
    if on_show_settings:
        settings_action.triggered.connect(on_show_settings)
    menu.addAction(settings_action)

    quit_action = QAction("Quit", app)
    if on_quit_callback:
        quit_action.triggered.connect(on_quit_callback)
    else:
        quit_action.triggered.connect(app.quit)
    menu.addAction(quit_action)

    tray.setContextMenu(menu)
    tray.show()

    return tray