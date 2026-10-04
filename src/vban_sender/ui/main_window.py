from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from vban_sender.ui.loopback_settings import LoopbackSettings
from vban_sender.ui.vban_settings import VBANSettings


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        # Set window properties
        self.setWindowTitle("VBAN Sender")

        # Set app stylesheet
        try:
            with open("src/style.qss", "r") as f:
                _styles = f.read()
            self.setStyleSheet(_styles)
        except FileNotFoundError:
            print("Stylesheet file 'style.qss' not found.")

        # Set main widget & layout
        # Content widgets will be added to the main layout
        _main_widget = QWidget()
        _main_layout = QVBoxLayout(_main_widget)
        self.setCentralWidget(_main_widget)

        _vban_settings = VBANSettings()
        _main_layout.addWidget(_vban_settings)

        _loopback_settings = LoopbackSettings()
        _main_layout.addWidget(_loopback_settings)