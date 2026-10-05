import json, os, subprocess
from pathlib import Path


VBAN_CONF_NAME = "10-vban-sender.conf"
# VBAN_CONF_NAME = "vban-mic.conf"

VBAN_CONF_BLANK_TEMPLATE = {
    "context.modules": [
        {
            "name": "libpipewire-module-vban-send",
            "args": {
                "destination.ip": "",
                "destination.port": "",
                "sess.name": "VBANSender",
                "audio.rate": 48000,
                "audio.channels": 2,
                "stream.props": {
                    "media.class": "Audio/Sink",
                    "node.name": "vban_sender",
                    "node.description": "VBAN Sender Output Sink"
                }
            }
        },
        {
            "name": "libpipewire-module-loopback",
            "args": {
                "node.name": "source_to_vban_bridge",
                "node.description": "Source to VBAN Bridge",
                "capture.props": {
                    "target.object": "@DEFAULT_AUDIO_SOURCE@"
                },
                "playback.props": {
                    "node.target": "vban_sender"
                }
            }
        }
    ]
}


class VBANConfModel:

    def __init__(self) -> None:
        super().__init__()

        vban_config_path = _get_pipewire_config_dir() / VBAN_CONF_NAME
        if not vban_config_path.is_file():
            # TODO: DO SOMETHING TO LOAD EMPTY TEMPLATE
            self._data = VBAN_CONF_BLANK_TEMPLATE
            return

        conf_dump = subprocess.run(
            ["spa-json-dump", vban_config_path],
            capture_output=True,
            text=True
        ).stdout

        self._data = json.loads(conf_dump)

    @property
    def data(self) -> dict:
        return self._data

    def get_by_path(self, path: list):
        """Retrieves a nested value given a list path."""
        current = self._data
        try:
            for key in path:
                current = current[key]
            return current
        except (KeyError, IndexError, TypeError):
            return None

    def update_by_path(self, path: list, value) -> None:
        """Updates the target key by the given path, and alerts all widgets."""
        if not path:
            return

        current = self._data
        # Travel down to the immediate parent (second-to-last item)
        try:
            for key in path[:-1]:
                current = current[key]
            target_key = path[-1]

            # Update the mutable reference in-place
            current[target_key] = value
        except (KeyError, IndexError, TypeError) as e:
            print(f"Error updating path {path}: {e}")

    def print_conf(self) -> None:
        """DEV METHOD FOR SEEING CONF MODEL"""
        print(json.dumps(self._data, indent=4))


def _get_pipewire_config_dir():
    """ADD DOC COMMENTS HERE"""
    # 1. Check if PIPEWIRE_CONFIG_DIR is set
    config_dir = os.environ.get("PIPEWIRE_CONFIG_DIR")
    if config_dir:
        return Path(config_dir) / "pipewire.conf.d"

    # 2. Check if XDG_CONFIG_HOME is set
    config_dir = os.environ.get("XDG_CONFIG_HOME")
    if config_dir:
        return Path(config_dir) / "pipewire" / "pipewire.conf.d"

    # 3. Fallback to standard config path
    return Path.home() / ".config" / "pipewire" / "pipewire.conf.d"


def get_audio_sources():
    """Gets a list of audio sources that can be assigned to the loopback module."""
    # Load in the data from the PipeWire "pw-dump" cli command
    # TODO: Add checks to make sure this command can be run + error handling
    pw_dump_info = subprocess.run(
        ["pw-dump"],
        capture_output=True,
        text=True
    ).stdout
    pw_dump_info = json.loads(pw_dump_info)

    # Search through the JSON data, getting only audio source interface nodes
    source_list = []
    for node in pw_dump_info:
        if node.get("type") == "PipeWire:Interface:Node":
            props = node.get("info", {}).get("props", {})
            if props.get("media.class") in ["Audio/Source", "Audio/Source/Virtual"]:
                source_list.append({
                    'name': props.get('node.name'),
                    'desc': props.get('node.description')
                })

    return source_list