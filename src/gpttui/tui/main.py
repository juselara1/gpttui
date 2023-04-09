from click import group
from gpttui.tui.front import front

@group()
def cli():
    pass

cli.add_command(front)
