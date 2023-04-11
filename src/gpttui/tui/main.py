"""
This file defines the main CLI.
"""
from click import group
from gpttui.tui.front import front
from gpttui.tui.config import css_config

@group()
def cli() -> None:
    css_config()

cli.add_command(front)
