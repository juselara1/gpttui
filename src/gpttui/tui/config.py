"""
This file defines the main configuration options for the TUI.
"""
from pathlib import Path
from pydantic import BaseModel
from typing import Type

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


def config_folder(config_path: Path) -> Path:
    """
    Setups the config folder and returns its path.

    Returns
    -------
    Path
        Configuration path.
    """
    if not config_path.exists():
        config_path.mkdir()
    return config_path


def config_file(path: Path, type: Type[BaseModel]) -> BaseModel:
    """
    Setups the config file given any configuration type.

    Parameters
    ----------
    path : str
        Configuration path.
    type : Type[ConfT]
        Configuration dataclass.

    Returns
    -------
    ConfT
        Loaded configuration.
    """
    if not path.exists():
        obj = type()
        with open(path, "w") as f:
            f.write(obj.json())
    else:
        obj = type.parse_file(path)
    return obj


def css_config(config_path: Path) -> Path:
    """
    Initializes the CSS configuration file.
    """
    cfg_path = config_folder(config_path)
    filename = cfg_path / "style.css"
    if not filename.exists():
        with open(filename, "w") as f:
            f.write(__CSS_CONFIG)
    return filename


def keybindings_config(config_path) -> KeyBindings:
    """
    Initializes the keybindings.
    """
    cfg_path = config_folder(config_path)
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
