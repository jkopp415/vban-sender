from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QPushButton

from vban_sender.core.pipewire_manager import VBANConfModel
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

        # Create the VBANConfModel object that will be passed to the settings panels
        self._vban_conf = VBANConfModel()

        # Set main widget & layout
        # Content widgets will be added to the main layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # Create VBAN sender and loopback settings panels
        self._vban_settings = VBANSettings(self._vban_conf)
        main_layout.addWidget(self._vban_settings)

        self._loopback_settings = LoopbackSettings(self._vban_conf)
        main_layout.addWidget(self._loopback_settings)

        # Create the save config panel
        save_panel = QWidget()
        save_panel_layout = QVBoxLayout(save_panel)
        main_layout.addWidget(save_panel)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self._on_save_button_clicked)
        save_panel_layout.addWidget(save_button)

    @Slot()
    def _on_save_button_clicked(self) -> None:
        self._vban_conf.print_conf()