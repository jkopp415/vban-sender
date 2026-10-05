from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSizePolicy

from vban_sender.core.pipewire_manager import VBANConfModel


class VBANSettings(QWidget):

    def __init__(self, vban_conf: VBANConfModel) -> None:
        super().__init__()
        self._vban_conf = vban_conf

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
        self._ip_input.textEdited.connect(
            lambda text: self._on_line_edit_changed(
                text, ["context.modules", 0, "args", "destination.ip"]
            )
        )
        dest_panel_layout.addWidget(self._ip_input)

        dest_panel_layout.addSpacing(25)

        port_label = QLabel("Port")
        dest_panel_layout.addWidget(port_label)

        self._port_input = QLineEdit()
        self._port_input.setMaxLength(4)
        self._port_input.setFixedWidth(40)
        # TODO: Add port input validation
        self._port_input.textEdited.connect(
            lambda text: self._on_line_edit_changed(
                int(text), ["context.modules", 0, "args", "destination.port"]
            )
        )
        dest_panel_layout.addWidget(self._port_input)

        self._set_settings()

    def _set_settings(self) -> None:
        """Runs upon initialization, gets the VBAN sender settings from
        PipeWire and fills the corresponding widgets."""
        self._ip_input.setText(self._vban_conf.get_by_path(
            ["context.modules", 0, "args", "destination.ip"]
        ))

        self._port_input.setText(str(self._vban_conf.get_by_path(
            ["context.modules", 0, "args", "destination.port"]
        )))

    @Slot(object, list)
    def _on_line_edit_changed(self, value: object, path: list):
        self._vban_conf.update_by_path(path, value)