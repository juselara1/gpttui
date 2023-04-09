from click import group
from gpttui.tui.front import front
from gpttui.tui.config import config_folder, css_config

@group()
def cli() -> None:
    path = config_folder()
    css_config(path)

cli.add_command(front)
