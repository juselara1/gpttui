"""
This file defines the main CLI.
"""
from click import group
from gpttui.tui.front import front
from gpttui.tui.init import init

@group()
def cli() -> None:
    ...


cli.add_command(front)
cli.add_command(init)
