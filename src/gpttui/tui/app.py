from textual.app import App, ComposeResult
from textual.widgets import Input, Markdown
from textual.containers import Content
from textual.events import Key
import os

class GptApp(App):
    CSS_PATH:str = os.path.join(os.environ["HOME"], "gpttui.css")

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
