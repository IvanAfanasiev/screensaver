import os
from PyQt5.QtWidgets import QWidget, QComboBox, QCheckBox, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from storage import Storage

storage = None 
settings = None 
background = None

class BackgroundWindow(QWidget):
    def __init__(self):
        super().__init__()
        global storage
        global settings
        global background

        storage = Storage()
        settings = storage.load_json("settings.json")
        background = self

        self.setWindowTitle("screensaver background")

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.resize(self.size())
        self.original_pixmap = QPixmap()
        self.pixmap = QPixmap()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

    def show(self):
        self.showFullScreen()

    def resizeEvent(self, event):
        self.label.resize(self.size())
        self.update_scaled_pixmap()
        
    def update_scaled_pixmap(self):
        if hasattr(self, "original_pixmap") and not self.original_pixmap.isNull():
            self.pixmap = self.original_pixmap.scaled(
                self.label.size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.FastTransformation
            )
            self.label.setPixmap(self.pixmap)

class SettingsWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        global background
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

        images_folder = "backgrounds"
        for file_path in storage.list_files(images_folder):
            if file_path.suffix.lower() in [".png", ".jpg", ".bmp"]:
                name = file_path.stem
                if name == "screenshot":
                    continue
                self.bg_combobox.addItem(name)
                self.bg_dict[name] = str(file_path.name)

        colors = ["Black", "White", "Red", "Green", "Blue"]
        for color in colors:
            name = color
            self.bg_combobox.addItem(name)
            self.bg_dict[name] = name


        self.bg_combobox.currentTextChanged.connect(
            lambda text: self.update_bg_preview(self.bg_dict.get(text))
        )

        option = os.path.splitext(settings["current-background"])
        index = self.bg_combobox.findText(option[0])
        if index != -1:
            self.bg_combobox.setCurrentIndex(index)
        else:
            self.bg_combobox.setCurrentIndex(0)
            self.update_bg_preview(self.bg_combobox.currentText())

        bg_layout.addWidget(self.bg_label)
        bg_layout.addWidget(self.bg_combobox)

        bg_layout.addWidget(self.bg_preview)
        layout.addLayout(bg_layout)

        # ----------------- Autorun -----------------
        self.autorun_checkbox = QCheckBox("Start with Windows")
        self.autorun_checkbox.setChecked(settings["autorun"])
        self.autorun_checkbox.stateChanged.connect(self.toggle_autorun)
        layout.addWidget(self.autorun_checkbox)
        self.setLayout(layout)
        if self.bg_dict:
            self.update_bg_preview(settings["current-background"])

    def update_bg_preview(self, value):
        if os.path.splitext(value)[1] != "":
            file_path = storage.get_file_path(value, folder="backgrounds")
            pixmap = QPixmap(str(file_path))
            if not pixmap.isNull():
                self.bg_preview.setPixmap(pixmap.scaled(
                    self.bg_preview.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
                ))
                self.bg_preview.setStyleSheet("")

                background.original_pixmap = pixmap
                background.update_scaled_pixmap()


                # background.pixmap = pixmap
                # background.label.setPixmap(background.pixmap)
                background.setStyleSheet("")
                settings["current-background"] = value
        else:
            self.bg_preview.setPixmap(QPixmap())
            self.bg_preview.setStyleSheet(f"background-color: {value};")
            background.label.setPixmap(QPixmap())
            background.setStyleSheet(f"background-color: {value};")
            settings["current-background"] = value
        storage.save_json("settings.json", settings)

    def toggle_autorun(self):
        settings["autorun"] = not settings["autorun"]
        storage.save_json("settings.json", settings)