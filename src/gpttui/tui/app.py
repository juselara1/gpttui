import os 
from pathlib import Path
from enum import Enum, auto
from typing import Any
from textual.app import App, ComposeResult
from textual.widgets import Input, Markdown
from textual.containers import Content
from textual.events import Key

class ModeEnum(Enum):
    INSERT = auto()
    NORMAL = auto()

class GptApp(App):
    CSS_PATH : Path = Path(os.environ["HOME"]) / ".config/gpttui/style.css"

    def __init__(self, *args: Any, **kwargs: Any):
        super(GptApp, self).__init__(*args, **kwargs)
        self.mode = ModeEnum.NORMAL

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter some text...")
        with Content(id="chat-container"):
            yield Markdown(id="chat")

    def on_mount(self) -> None:
        self.query_one(Markdown).update("Waiting for response...")

    def on_key(self, event: Key) -> None:
        inp = self.query_one(Input)
        chat = self.query_one(Markdown)
        if event.key == "enter":
            chat.update(inp.value)
            inp.action_delete_right_all()
            inp.action_delete_left_all()
        elif event.key == "i":
            inp.focus()
        elif event.key == "escape":
            inp.reset_focus()
        elif event.key == "y":
            ...
        elif event.key == "p":
            ...
        elif event.key == "c":
            ...
        elif event.key == "q":
            ...
