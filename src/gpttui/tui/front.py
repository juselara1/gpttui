"""
This file defines the CLI options in the front subcommand.
"""
import os
from pathlib import Path
from click import option, command
from pydantic import BaseModel
from gpttui.database.base import AbstractDB, DatabasesEnum
from gpttui.database.sqlite import SqliteDB
from gpttui.models.base import AbstractModel, ModelsEnum
from gpttui.models.chatsonic import ChatSonicConf, ChatSonicModel
from gpttui.models.colossal import ColossalConf, ColossalModel
from gpttui.models.openai import OpenAIModel, OpenAIConf
from gpttui.tui.app import GptApp
from gpttui.tui.config import config_file, css_config, keybindings_config
from typing import Dict, Type

DBS: Dict[DatabasesEnum, Type[AbstractDB]] = {
        DatabasesEnum.SQLITE: SqliteDB
        }
MODELS: Dict[ModelsEnum, Type[AbstractModel]] = {
        ModelsEnum.OPENAI: OpenAIModel,
        ModelsEnum.CHATSONIC: ChatSonicModel,
        ModelsEnum.COLOSSAL: ColossalModel
        }
CONFS: Dict[ModelsEnum, Type[BaseModel]] = {
        ModelsEnum.OPENAI: OpenAIConf,
        ModelsEnum.CHATSONIC: ChatSonicConf,
        ModelsEnum.COLOSSAL: ColossalConf
        }

@command()
@option(
    "--database_kind",
    type=DatabasesEnum,
    default=DatabasesEnum.SQLITE,
    help="Database to store the messages."
    )
@option(
    "--database_name",
    type=str,
    default="database.sqlite",
    help="Connection string for the database."
    )
@option(
    "--session",
    type=str,
    default="default_session",
    help="Session (chat) to use."
    )
@option(
    "--model_kind",
    type=ModelsEnum,
    default=ModelsEnum.OPENAI,
    help="Which model to use."
    )
@option(
    "--context",
    type=str,
    default="You are an AI assistant",
    help="Context for the model."
    )
@option(
    "--config_path",
    type=Path,
    default=Path(os.environ["HOME"]) / ".config/gpttui",
    help="Folder to save gpttui data."
    )
@option(
    "--model_config",
    type=str,
    default="openai.json",
    help="Context for the model."
    )
def front(
    database_kind: DatabasesEnum,
    database_name: str,
    session: str,
    model_kind: ModelsEnum,
    context: str,
    config_path: Path,
    model_config: str
    ) -> None:
    """
    Determines what to do when the front subcommand is launched.

    Parameters
    ----------
    database_kind : DatabasesEnum
        Which database to use.
    database_name : str
        Connection string to the database.
    session : str
        Session name.
    model_kind : ModelsEnum
        Which model to use.
    model_name : str
        Model name.
    context : str
        Context for the model.
    config_folder : Path
        Folder to save gpttui data.
    model_config : str
        Json file with the model's configuration.
    """
    css_path = css_config(config_path)
    keybindings = keybindings_config(config_path)
    db = (
            DBS[database_kind]()
            .setup(database=str(config_path / database_name))
            )
    db.create_session(session_name=session)
    cfg = config_file(config_path / model_config, CONFS[model_kind])

    model = (
            MODELS[model_kind]()
            .add_context(context=context)
            .setup(config=cfg, database=db, session_name=session)
            )
    app = (
            GptApp
            .setup_cls(css_path=css_path, keybindings=keybindings)()
            .setup(model=model)
            )
    app.run()
