from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QSizePolicy

from vban_sender.core import pipewire_manager


class LoopbackSettings(QWidget):

    def __init__(self) -> None:
        super().__init__()

        layout = QVBoxLayout(self)

        # ===== INPUT DEVICE SETTINGS =====
        input_panel = QWidget()
        input_panel.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        input_panel_layout = QHBoxLayout(input_panel)
        layout.addWidget(input_panel)

        input_device_label = QLabel("Target Object")
        input_panel_layout.addWidget(input_device_label)

        self._input_device_combo = QComboBox()
        self._input_device_combo.currentIndexChanged.connect(self.on_index_changed)
        input_panel_layout.addWidget(self._input_device_combo)
        self._initialize_input_device_combo()

        self._initialize_settings()

    def _initialize_input_device_combo(self) -> None:
        """Gets a list of audio sources from the system to populate the input device combo."""
        # Add the default audio source PipeWire var to the combo first
        self._input_device_combo.addItem(
            "Default Audio Source",
            userData="@DEFAULT_AUDIO_SOURCE@"
        )

        # Then add all recognized audio sources recognized by PipeWire
        for device in pipewire_manager.get_audio_sources():
            self._input_device_combo.addItem(
                device['desc'],
                userData=device['name']
            )

    def _initialize_settings(self) -> None:
        loopback_settings = pipewire_manager.get_vban_config()["loopback"]

        if "target.object" in loopback_settings:
            idx = self._input_device_combo.findData(loopback_settings["target.object"])
            if idx != -1:
                self._input_device_combo.setCurrentIndex(idx)

    @Slot(int)
    def on_index_changed(self, _index: int) -> None:
        pass