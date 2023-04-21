"""
This file defines the main TUI App.
"""
import os, re
import pyperclip
from pathlib import Path
from enum import Enum, auto
from typing import Any
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
    """
    Static container for the normal mode.
    """
    ...

class InsertIndicator(Static):
    """
    Static container for the insert mode.
    """
    ...

class UserInput(Input):
    """
    Represents the text input.
    """
    ...

class Prompt(Static):
    """
    The prompt contains the mode indicators and the text input.
    """
    def compose(self) -> ComposeResult:
        yield NormalIndicator("NORMAL", id="normal-indicator")
        yield InsertIndicator("INSERT", id="insert-indicator")
        yield Input(placeholder="Enter some text...")

class UserText(Static):
    """
    Static container to display the sender.
    """
    ...

class Message(Static):
    """
    A message contains the the sender and its text.

    Parameters
    ----------
    user : str
        Sender.
    message : str
        Text of the message.
    """

    def __init__(self, user:str, message: str, *args: Any, **kwargs: Any):
        super(Message, self).__init__(*args, **kwargs)
        self.user = user
        self.message = message

    def compose(self) -> ComposeResult:
        """
        Generator with the message components.

        Yields
        ------
        ComposeResult:
            Widgets in the message.

        """
        yield UserText(self.user)
        # BUG: seems like textual isn't able to render inline code compose markdowns.
        try:
            md = Markdown()
            md.update(self.message)
        except:
            md = Static(self.message)
        yield md

class Messages(Container):
    """
    A container that stores all messages.
    """

    def add_message(self, msg: str, user: str):
        """
        This method dynamically adds a message.

        Parameters
        ----------
        msg : str
            Message to display.
        user : str
            Sender of the message.
        """
        self.mount(Message(user=user, message=msg))
        self.scroll_end()

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

    async def on_key(self, event: Key) -> None:
        """
        Callback that is called when a key is pressed.

        Parameters
        ----------
        event : Key
            Event related to the key that was pressed.
        """
        if self.mode == ModeEnum.NORMAL:
            await self.handle_normal(event)
        elif self.mode == ModeEnum.INSERT:
            await self.handle_insert(event)

    async def handle_normal(self, event: Key) -> None:
        """
        Determines what to do in normal mode.

        Parameters
        ----------
        event : Key
            Event related to the key that was pressed.
        """
        f = self.normal_commands.get(event.key)
        if f is not None: await f()

    async def handle_insert(self, event: Key) -> None:
        """
        Determines what to do in insert mode.

        Parameters
        ----------
        event : Key
            Event related to the key that was pressed.
        """
        f = self.insert_commands.get(event.key)
        if f is not None: await f()

    async def insert(self):
        """
        Changes to insert mode.
        """
        self.add_class("insert-mode")
        self.query_one(Input).focus()
        self.mode = ModeEnum.INSERT

    async def clear(self):
        """
        Clears the historical messages.
        """
        self.query_one(Messages) #TODO

    async def yank(self):
        """
        Copies the last message into the clipboard.
        """
        msgs = self.model.database.get_messages(self.model.session_name)
        pyperclip.copy(msgs.values[-1].content)

    async def paste(self):
        """
        Pastes the clipboard into the prompt.
        """
        clipboard_text = pyperclip.paste()
        self.query_one(Input).insert_text_at_cursor(clipboard_text)

    async def normal(self):
        """
        Switch to normal mode.
        """
        self.remove_class("insert-mode")
        self.query_one(Input).reset_focus()
        self.mode = ModeEnum.NORMAL

    async def quit(self):
        """
        Exit the app.
        """
        self.model.database.close()
        self.exit()

    async def delete(self):
        """
        Deletes the prompt.
        """
        inp = self.query_one(Input)
        inp.action_delete_right_all()
        inp.action_delete_left_all()

    async def send(self):
        """
        Sends the text in the prompt to the model and shows the response.
        """
        inp = self.query_one(Input)
        text = inp.value
        messages = self.query_one(Messages)
        inp.action_delete_right_all()
        inp.action_delete_left_all()
        messages.add_message(msg=text, user="User")
        answer = await self.model.get_answer(text)
        messages.add_message(msg=answer, user="Assistant")
