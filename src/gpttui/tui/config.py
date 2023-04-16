"""
This file defines the main configuration options for the TUI.
"""
import os
from pathlib import Path
from pydantic import BaseModel

__CSS_CONFIG = """
Prompt {
    dock: bottom;
    layout: horizontal;
    padding: 0;
    margin: 0;
}

#normal-indicator {
    dock: left;
    width: 6%;
    height: 100%;
    background: #8EC07C;
    color: #3C3836;
    content-align: center middle;
    padding: 0;
    margin: 0 0 0 1;
}

#insert-indicator {
    dock: left;
    width: 6%;
    height: 100%;
    background: #458588;
    color: #3C3836;
    content-align: center middle;
    padding: 0;
    margin: 0 0 0 1;
    display: none;
}

Input {
    dock: right;
    width: 94%;
    padding: 0 0 0 1;
    margin: 0;
}

.insert-mode #normal-indicator {
    display: none;
}

.insert-mode #insert-indicator {
    display: block;
}

Message {
    layout: horizontal;
    padding: 1 0 0 0;
    margin: 0;
}

UserText {
    dock: left;
    content-align: center middle;
    background: #B8BB26;
    color: #3C3836;
    padding: 0;
    margin: 0 0 0 1;
    height: 100%;
    width: 6%;
}

UserMessage {
    dock: right;
    width: 94%;
    padding: 0 0 0 1;
    margin: 0;
}
"""

class KeyBindings(BaseModel):
    """
    Dataclass that represents the possible keybindings.
    """
    insert: str
    normal: str
    yank: str
    paste: str
    clear: str
    quit: str
    send: str
    delete: str

def config_folder() -> Path:
    """
    Setups the config folder and returns its path.

    Returns
    -------
    Path
        Configuration path.
    """
    home_path = os.environ["HOME"]
    cfg_path = Path(os.path.join(home_path, ".config/gpttui"))
    if not cfg_path.exists():
        cfg_path.mkdir()
    return cfg_path

def css_config():
    """
    Initializes the CSS configuration file.
    """
    cfg_path = config_folder()
    filename = cfg_path / "style.css"
    if not filename.exists():
        with open(filename, "w") as f:
            f.write(__CSS_CONFIG)

def keybindings_config() -> KeyBindings:
    """
    Initializes the keybindings.
    """
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
                send="enter",
                delete="d",
                )
        with open(filename, "w") as f:
            f.write(keybindings.json())
    else:
        keybindings = KeyBindings.parse_file(filename)
    return keybindings
