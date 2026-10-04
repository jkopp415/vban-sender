from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSizePolicy

from vban_sender.core import pipewire_manager


class VBANSettings(QWidget):

    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)

        # ===== DESTINATION OPTIONS =====
        dest_panel = QWidget()
        dest_panel.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        dest_panel_layout = QHBoxLayout(dest_panel)
        layout.addWidget(dest_panel)

        ip_label = QLabel("Destination IP Address")
        dest_panel_layout.addWidget(ip_label)

        self._ip_input = QLineEdit()
        self._ip_input.setMaxLength(15)
        self._ip_input.setFixedWidth(125)
        # TODO: Add IP input validation
        dest_panel_layout.addWidget(self._ip_input)

        dest_panel_layout.addSpacing(25)

        port_label = QLabel("Port")
        dest_panel_layout.addWidget(port_label)

        self._port_input = QLineEdit()
        self._port_input.setMaxLength(4)
        self._port_input.setFixedWidth(40)
        # TODO: Add port input validation
        dest_panel_layout.addWidget(self._port_input)

        self._initialize_settings()

    def _initialize_settings(self) -> None:
        vban_settings = pipewire_manager.get_vban_config()['vban-send']

        if "destination.ip" in vban_settings:
            self._ip_input.setText(vban_settings["destination.ip"])

        if "destination.port" in vban_settings:
            self._port_input.setText(str(vban_settings["destination.port"]))