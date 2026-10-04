from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QSizePolicy


class VBANSettings(QWidget):

    def __init__(self) -> None:
        super().__init__()

        _layout = QVBoxLayout(self)

        # ===== DESTINATION OPTIONS =====
        _dest_panel = QWidget()
        _dest_panel.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        _dest_panel_layout = QHBoxLayout(_dest_panel)
        _layout.addWidget(_dest_panel)

        _ip_label = QLabel("Destination IP Address")
        _dest_panel_layout.addWidget(_ip_label)

        _ip_input = QLineEdit()
        _ip_input.setMaxLength(15)
        _ip_input.setFixedWidth(125)
        # TODO: Add IP input validation
        _dest_panel_layout.addWidget(_ip_input)

        _dest_panel_layout.addSpacing(25)

        _port_label = QLabel("Port")
        _dest_panel_layout.addWidget(_port_label)

        _port_input = QLineEdit()
        _port_input.setMaxLength(4)
        _port_input.setFixedWidth(40)
        # TODO: Add port input validation
        _dest_panel_layout.addWidget(_port_input)