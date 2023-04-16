"""
This file defines the main TUI App.
"""
import os 
import pyperclip
from pathlib import Path
from enum import Enum, auto
from typing import Any, Optional
from textual.app import App, ComposeResult
from textual.widgets import Input, Markdown, Static
from textual.containers import Container
from textual.events import Key
from gpttui.models.base import AbstractModel
from gpttui.tui.config import KeyBindings, keybindings_config

class ModeEnum(Enum):
    """
    This enum represents the possible modes of the application.
    """
    INSERT = auto()
    NORMAL = auto()

class NormalIndicator(Static):
    ...

class InsertIndicator(Static):
    ...

class UserInput(Input):
    ...

class Prompt(Static):
    def compose(self) -> ComposeResult:
        yield NormalIndicator("NORMAL", id="normal-indicator")
        yield InsertIndicator("INSERT", id="insert-indicator")
        yield Input(placeholder="Enter some text...")

class UserText(Static):
    ...

class UserMessage(Static):
    ...

class Message(Static):

    def __init__(self, user:str, message: str, *args: Any, **kwargs: Any):
        super(Message, self).__init__(*args, **kwargs)
        self.user = user
        self.message = message

    def compose(self) -> ComposeResult:
        yield UserText(self.user)
        yield UserMessage(self.message)

class Messages(Container):

    def add_message(self, msg: str, user: str):
        self.mount(Message(user=user, message=msg))

class GptApp(App):
    """
    This class defines the TUI App.

    Parameters
    ----------
    CSS_PATH : Path
        Path for the CSS styling file.
    KEYBINDINGS : KeyBindings
        Keybindings to use in the application.
    model : AbstractModel
        Model to use in the App.
    mode : ModeEnum
        Current mode in the App.
    chat_text : str
        Visible text that is show in the chat.
    normal_commands : str
        Mapping between a keybinding and its function in normal mode.
    insert_commands : str
        Mapping between a keybinding and its function in insert mode.
    """
    CSS_PATH : Path = Path(os.environ["HOME"]) / ".config/gpttui/style.css"
    KEYBINDINGS : KeyBindings = keybindings_config()
    model: AbstractModel

    def __init__(self, *args: Any, **kwargs: Any):
        super(GptApp, self).__init__(*args, **kwargs)
        self.mode = ModeEnum.NORMAL
        self.normal_commands = {
                self.KEYBINDINGS.insert: self.insert,
                self.KEYBINDINGS.quit: self.quit,
                self.KEYBINDINGS.yank: self.yank,
                self.KEYBINDINGS.paste: self.paste,
                self.KEYBINDINGS.clear: self.clear,
                self.KEYBINDINGS.delete: self.delete
                }
        self.insert_commands = {
                self.KEYBINDINGS.normal: self.normal,
                self.KEYBINDINGS.send: self.send,
                }

    def setup(self, model: AbstractModel) -> "GptApp":
        """
        Setups the App.

        Parameters
        ----------
        model : AbstractModel
            Specifies the model to use.

        Returns
        -------
        GptApp
            Instance of the app to use as a builder.
        """
        self.model = model
        return self

    def compose(self) -> ComposeResult:
        """
        Generator with the TUI components.

        Yields
        ------
        ComposeResult
            TUI components.
        """
        yield Prompt()
        yield Messages()

    def on_key(self, event: Key) -> None:
        """
        Callback that is called when a key is pressed.

        Parameters
        ----------
        event : Key
            Event related to the key that was pressed.
        """
        if self.mode == ModeEnum.NORMAL:
            self.handle_normal(event)
        elif self.mode == ModeEnum.INSERT:
            self.handle_insert(event)

    def handle_normal(self, event: Key) -> None:
        """
        Determines what to do in normal mode.

        Parameters
        ----------
        event : Key
            Event related to the key that was pressed.
        """
        f = self.normal_commands.get(event.key)
        if f is not None: f()

    def handle_insert(self, event: Key) -> None:
        """
        Determines what to do in insert mode.

        Parameters
        ----------
        event : Key
            Event related to the key that was pressed.
        """
        f = self.insert_commands.get(event.key)
        if f is not None: f()

    def insert(self):
        """
        Changes to insert mode.
        """
        self.add_class("insert-mode")
        self.query_one(Input).focus()
        self.mode = ModeEnum.INSERT

    def clear(self):
        """
        Clears the historical messages.
        """
        self.chat_text = ""
        self.query_one(Markdown).update(self.chat_text)

    def yank(self):
        """
        Copies the last message into the clipboard.
        """
        msgs = self.model.database.get_messages(self.model.session_name)
        pyperclip.copy(msgs.values[-1].content)

    def paste(self):
        """
        Pastes the clipboard into the prompt.
        """
        clipboard_text = pyperclip.paste()
        self.query_one(Input).insert_text_at_cursor(clipboard_text)

    def normal(self):
        """
        Switch to normal mode.
        """
        self.remove_class("insert-mode")
        self.query_one(Input).reset_focus()
        self.mode = ModeEnum.NORMAL

    def quit(self):
        """
        Exit the app.
        """
        self.model.database.close()
        self.exit()

    def delete(self):
        """
        Deletes the prompt.
        """
        inp = self.query_one(Input)
        inp.action_delete_right_all()
        inp.action_delete_left_all()

    def send(self):
        """
        Sends the text in the prompt to the model and shows the response.
        """
        inp = self.query_one(Input)
        text = inp.value
        inp.action_delete_right_all()
        inp.action_delete_left_all()
        answer = self.model.get_answer(text)
        messages = self.query_one(Messages)
        messages.add_message(msg=text, user="User")
        messages.add_message(msg=answer, user="Assistant")
        messages.scroll_end()
