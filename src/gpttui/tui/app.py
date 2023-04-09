import os 
import pyperclip
from pathlib import Path
from enum import Enum, auto
from typing import Any
from textual.app import App, ComposeResult
from textual.widgets import Input, Markdown
from textual.events import Key
from gpttui.models.base import AbstractModel
from gpttui.tui.config import KeyBindings, keybindings_config

class ModeEnum(Enum):
    INSERT = auto()
    NORMAL = auto()

class GptApp(App):
    CSS_PATH : Path = Path(os.environ["HOME"]) / ".config/gpttui/style.css"
    KEYBINDINGS : KeyBindings = keybindings_config()
    model: AbstractModel

    def __init__(self, *args: Any, **kwargs: Any):
        super(GptApp, self).__init__(*args, **kwargs)
        self.mode = ModeEnum.NORMAL
        self.chat_text = ""
        self.normal_commands = {
                self.KEYBINDINGS.insert: self.insert,
                self.KEYBINDINGS.quit: self.quit,
                self.KEYBINDINGS.yank: self.yank,
                self.KEYBINDINGS.paste: self.paste,
                self.KEYBINDINGS.clear: self.clear
                }
        self.insert_commands = {
                self.KEYBINDINGS.normal: self.normal,
                self.KEYBINDINGS.send: self.send
                }

    def setup(self, model: AbstractModel) -> "GptApp":
        self.model = model
        return self

    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter some text...")
        yield Markdown()

    def on_mount(self) -> None:
        self.query_one(Markdown).update("Waiting for response...")

    def on_key(self, event: Key) -> None:
        if self.mode == ModeEnum.NORMAL:
            self.handle_normal(event)
        else:
            self.handle_insert(event)

    def handle_normal(self, event: Key) -> None:
        f = self.normal_commands.get(event.key)
        if f is not None: f()

    def handle_insert(self, event: Key) -> None:
        f = self.insert_commands.get(event.key)
        if f is not None: f()

    def insert(self):
        self.query_one(Input).focus()
        self.mode = ModeEnum.INSERT

    def clear(self):
        self.chat_text = ""
        self.query_one(Markdown).update(self.chat_text)

    def yank(self):
        msgs = self.model.database.get_messages(self.model.session_name)
        pyperclip.copy(msgs.values[-1].content)

    def paste(self):
        clipboard_text = pyperclip.paste()
        self.query_one(Input).insert_text_at_cursor(clipboard_text)

    def normal(self):
        self.query_one(Input).reset_focus()
        self.mode = ModeEnum.NORMAL

    def quit(self):
        self.model.database.close()
        self.exit()

    def send(self):
        chat = self.query_one(Markdown)
        inp = self.query_one(Input)
        text = inp.value
        inp.action_delete_right_all()
        inp.action_delete_left_all()
        answer = self.model.get_answer(text)
        self.chat_text += f"### User\n{text}\n"
        self.chat_text += f"### Assistant\n{answer}\n"
        chat.update(self.chat_text)
