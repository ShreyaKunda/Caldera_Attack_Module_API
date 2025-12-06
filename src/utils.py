import json
from pathlib import Path

CONFIG_PATH = Path("config/settings.json")
DEFAULT_MAPPING = Path("config/ability_mapping.json")

def load_config():
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config file not found: {CONFIG_PATH.resolve()}")
    with open(CONFIG_PATH, "r") as f:
        cfg = json.load(f)
    return cfg

def load_mapping(path=None):
    p = DEFAULT_MAPPING if path is None else Path(path)
    if not p.exists():
        return {}
    with open(p, "r") as f:
        return json.load(f)
