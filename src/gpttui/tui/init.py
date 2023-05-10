"""
This file defines the CLI options in the front subcommand.
"""
import os
from pathlib import Path
from click import option, command
from pydantic import BaseModel
from gpttui.models.base import  ModelsEnum
from gpttui.models.chatsonic import ChatSonicConf
from gpttui.models.colossal import ColossalConf
from gpttui.models.openai import OpenAIConf
from gpttui.tui.config import config_file, css_config, keybindings_config
from typing import Dict, Type

CONFS: Dict[ModelsEnum, Type[BaseModel]] = {
    ModelsEnum.OPENAI: OpenAIConf,
    ModelsEnum.CHATSONIC: ChatSonicConf,
    ModelsEnum.COLOSSAL: ColossalConf,
}

@command()
@option(
    "--model_kind",
    type=ModelsEnum,
    default=ModelsEnum.OPENAI,
    help="Which model to use.",
)
@option(
    "--config_path",
    type=Path,
    default=Path(os.environ["HOME"]) / ".config/gpttui",
    help="Folder to save gpttui data.",
)
@option(
    "--model_config", type=str, default="openai.json", help="Context for the model."
)
def init(
    model_kind: ModelsEnum,
    config_path: Path,
    model_config: str,
) -> None:
    """
    Generates configuration files.

    Parameters
    ----------
    model_kind : ModelsEnum
        Which model to use.
    config_path : Path
        Folder to save gpttui data.
    model_config : str
        Json file with the model's configuration.
    """
    css_config(config_path)
    keybindings_config(config_path)
    config_file(config_path / model_config, CONFS[model_kind])
