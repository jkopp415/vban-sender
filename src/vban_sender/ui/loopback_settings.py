from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QSizePolicy

from vban_sender.core import audio_manager


class LoopbackSettings(QWidget):

    def __init__(self) -> None:
        super().__init__()

        _layout = QVBoxLayout(self)

        # ===== INPUT DEVICE SETTINGS =====
        _input_panel = QWidget()
        _input_panel.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        _input_panel_layout = QHBoxLayout(_input_panel)
        _layout.addWidget(_input_panel)

        _input_device_label = QLabel("Target Object")
        _input_panel_layout.addWidget(_input_device_label)

        self._input_device_combo = QComboBox()
        self._input_device_combo.currentIndexChanged.connect(self.on_index_changed)
        _input_panel_layout.addWidget(self._input_device_combo)
        self._initialize_input_device_combo()

    def _initialize_input_device_combo(self) -> None:
        # Add the default audio source PipeWire var to the combo first
        self._input_device_combo.addItem(
            "Default Audio Source",
            userData="@DEFAULT_AUDIO_SOUCE@"
        )

        # Then add all recognized audio sources recognized by PipeWire
        for device in audio_manager.get_audio_sources():
            self._input_device_combo.addItem(
                device['desc'],
                userData=device['name']
            )

    @Slot(int)
    def on_index_changed(self, _index: int) -> None:
        pass