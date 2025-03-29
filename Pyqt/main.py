import sys
import json
import time
import psutil
import threading
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QMenu
from PyQt6.QtGui import QAction, QMouseEvent
from PyQt6.QtCore import Qt, QPoint
from Pyqt.settings import SettingsWindow

CONFIG_FILE = "config.json"

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.load_config()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.offset = QPoint()

        layout = QVBoxLayout()
        self.download_label = QLabel("↓ 0.00 KBps", self)
        self.upload_label = QLabel("↑ 0.00 KBps", self)

        self.apply_styles()

        layout.addWidget(self.download_label)
        layout.addWidget(self.upload_label)
        self.setLayout(layout)

        self.start_monitoring()

    def load_config(self):
        try:
            with open(CONFIG_FILE, "r") as file:
                self.config = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.config = {
                "unit": "KBps",
                "background_opacity": 0.7,
                "text_color": "#FFFFFF"
            }
            with open(CONFIG_FILE, "w") as file:
                json.dump(self.config, file, indent=4)

    def apply_styles(self):
        self.setStyleSheet(f"background: rgba(0, 0, 0, {self.config['background_opacity']});")
        text_color = self.config["text_color"]
        self.download_label.setStyleSheet(f"color: {text_color}; font-size: 14px; font-weight: bold;")
        self.upload_label.setStyleSheet(f"color: {text_color}; font-size: 14px; font-weight: bold;")

    def update_speed(self):
        units = {
            "Kbps": 1024, "Mbps": 1024**2, "Gbps": 1024**3,
            "KBps": 1024, "MBps": 1024**2, "GBps": 1024**3
        }

        while True:
            divisor = units.get(self.config["unit"], 1024)
            old_data = psutil.net_io_counters()
            time.sleep(1)
            new_data = psutil.net_io_counters()

            if self.config["unit"] in ["Kbps", "Mbps", "Gbps"]:
                download_speed = ((new_data.bytes_recv - old_data.bytes_recv) * 8) / divisor
                upload_speed = ((new_data.bytes_sent - old_data.bytes_sent) * 8) / divisor
            else:
                download_speed = (new_data.bytes_recv - old_data.bytes_recv) / divisor
                upload_speed = (new_data.bytes_sent - old_data.bytes_sent) / divisor

            self.download_label.setText(f"↓ {download_speed:.2f} {self.config['unit']}")
            self.upload_label.setText(f"↑ {upload_speed:.2f} {self.config['unit']}")

    def start_monitoring(self):
        threading.Thread(target=self.update_speed, daemon=True).start()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        settings_action = QAction("Settings", self)
        close_action = QAction("Close", self)

        settings_action.triggered.connect(self.open_settings)
        close_action.triggered.connect(self.close)

        menu.addAction(settings_action)
        menu.addAction(close_action)
        menu.exec(event.globalPos())

    def open_settings(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
