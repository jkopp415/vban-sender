import json, subprocess


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