"""
This file defines the main CLI.
"""
from click import group
from gpttui.tui.front import front

@group()
def cli() -> None:
    ...

cli.add_command(front)
