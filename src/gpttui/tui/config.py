import os
from pathlib import Path
from pydantic import BaseModel

class KeyBindings(BaseModel):
    insert: str
    normal: str
    yank: str
    paste: str
    clear: str
    quit: str
    send: str

def config_folder() -> Path:
    home_path = os.environ["HOME"]
    cfg_path = Path(os.path.join(home_path, ".config/gpttui"))
    if not cfg_path.exists():
        cfg_path.mkdir()
    return cfg_path

def css_config():
    cfg = """Input {
    dock: bottom;
}"""
    cfg_path = config_folder()
    filename = cfg_path / "style.css"
    if not filename.exists():
        with open(filename, "w") as f:
            f.write(cfg)

def keybindings_config() -> KeyBindings:
    cfg_path = config_folder()
    filename = cfg_path / "keybindings.json"
    if not filename.exists():
        filename.touch()
        keybindings = KeyBindings(
                insert="i",
                normal="escape",
                yank="y",
                paste="p",
                clear="c",
                quit="q",
                send="enter"
                )
        with open(filename, "w") as f:
            f.write(keybindings.json())
    else:
        keybindings = KeyBindings.parse_file(filename)
    return keybindings
