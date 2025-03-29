import json
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QColorDialog, QComboBox, QSlider
from PyQt6.QtCore import Qt

CONFIG_FILE = "config.json"

class SettingsWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("Settings")
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout()

        self.color_button = QPushButton("Change Text Color", self)
        self.color_button.clicked.connect(self.change_text_color)
        layout.addWidget(self.color_button)

        self.opacity_label = QLabel("Background Opacity:", self)
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.opacity_slider.setMinimum(0)
        self.opacity_slider.setMaximum(100)
        self.opacity_slider.setValue(int(self.main_window.config["background_opacity"] * 100))
        self.opacity_slider.valueChanged.connect(self.change_opacity)

        layout.addWidget(self.opacity_label)
        layout.addWidget(self.opacity_slider)

        self.unit_label = QLabel("Select Unit:", self)
        self.unit_combo = QComboBox(self)
        self.unit_combo.addItems(["Kbps", "Mbps", "Gbps", "KBps", "MBps", "GBps"])
        self.unit_combo.setCurrentText(self.main_window.config["unit"])
        self.unit_combo.currentTextChanged.connect(self.change_unit)

        layout.addWidget(self.unit_label)
        layout.addWidget(self.unit_combo)

        self.save_button = QPushButton("Save & Apply", self)
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def change_text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.main_window.config["text_color"] = color.name()
            self.main_window.apply_styles()

    def change_opacity(self, value):
        self.main_window.config["background_opacity"] = value / 100
        self.main_window.apply_styles()

    def change_unit(self, unit):
        self.main_window.config["unit"] = unit

    def save_settings(self):
        with open(CONFIG_FILE, "w") as file:
            json.dump(self.main_window.config, file, indent=4)
        self.close()
