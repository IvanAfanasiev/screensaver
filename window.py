import os
from PyQt5.QtWidgets import QWidget, QComboBox,  QApplication, QLineEdit, QCheckBox, QFileDialog, QHBoxLayout, QPushButton, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QDoubleValidator

current_background = "Black"
autorun = False

class BackgroundWindow(QWidget):
    def __init__(self):
        super().__init__()
        global current_background

        self.setWindowTitle("screensaver background")

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.pixmap = QPixmap(current_background)
        self.label.setPixmap(self.pixmap)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.settings_window = None

    def show(self):
        print(current_background)
        self.setStyleSheet(f"background-color: {current_background};")
        self.showFullScreen()

class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        global current_background

        self.setAttribute(Qt.WA_QuitOnClose, False)

        self.setWindowTitle("screensaver settings")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        # ----------------- Background -----------------
        bg_layout = QHBoxLayout()
        self.bg_label = QLabel("Background:")
        self.bg_preview = QLabel()
        self.bg_preview.setFixedSize(400, 250)
        self.bg_preview.setFrameShape(QLabel.Box)

        self.bg_combobox = QComboBox()
        self.bg_dict = {}

        colors = ["Black", "White", "Red", "Green", "Blue"]
        for color in colors:
            name = color
            self.bg_combobox.addItem(name)
            self.bg_dict[name] = name

        self.bg_combobox.currentTextChanged.connect(
            lambda text: self.update_bg_preview(self.bg_dict.get(text))
        )

        bg_layout.addWidget(self.bg_label)
        bg_layout.addWidget(self.bg_combobox)

        bg_layout.addWidget(self.bg_preview)
        layout.addLayout(bg_layout)

        # ----------------- Autorun -----------------
        self.autorun_checkbox = QCheckBox("Start with Windows")
        self.autorun_checkbox.setChecked(autorun)
        self.autorun_checkbox.stateChanged.connect(self.toggle_autorun)
        layout.addWidget(self.autorun_checkbox)

        self.setLayout(layout)
        if self.bg_dict:
            self.update_bg_preview(current_background)

    def update_bg_preview(self, value):
        global current_background
        self.bg_preview.setPixmap(QPixmap())
        self.bg_preview.setStyleSheet(f"background-color: {value};")
        current_background = value

    def toggle_autorun(self):
        global autorun
        autorun = not autorun