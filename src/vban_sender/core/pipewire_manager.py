import json, os, subprocess
from pathlib import Path


VBAN_CONF_NAME = "vban-mic.conf"


def get_pipewire_config_dir() -> Path:
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


def get_vban_config() -> dict:
    conf_list = {
        "vban-send": {},
        "loopback": {}
    }

    # Make sure the conf file actually exists
    vban_config_path = get_pipewire_config_dir() / VBAN_CONF_NAME
    if not vban_config_path.is_file():
        return conf_list

    # Get the conf file's json data
    conf_dump = subprocess.run(
        ["spa-json-dump", vban_config_path],
        capture_output=True,
        text=True
    ).stdout
    conf_dump = json.loads(conf_dump)

    for module in conf_dump.get("context.modules", []):
        args = module.get("args", {})

        # TODO: Add addl. conf settings below

        # Check for vban-send module's destination ip
        if "destination.ip" in args:
            conf_list["vban-send"]['destination.ip'] = args['destination.ip']

        # Check for vban-send module's destination port
        if "destination.port" in args:
            conf_list["vban-send"]['destination.port'] = args['destination.port']

        # Check for loopback module's capture props
        capture_props = args.get("capture.props", {})
        if "target.object" in capture_props:
            conf_list["loopback"]['target.object'] = capture_props['target.object']

    return conf_list


def get_audio_sources() -> list[dict]:
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