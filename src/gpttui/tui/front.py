"""
This file defines the CLI options in the front subcommand.
"""
import os
from pathlib import Path
from click import option, command
from gpttui.database.base import AbstractDB, DatabasesEnum
from gpttui.database.sqlite import SqliteDB
from gpttui.models.base import AbstractModel, ModelsEnum
from gpttui.models.openai import OpenAIModel
from gpttui.tui.app import GptApp
from typing import Dict, Type

DBS: Dict[DatabasesEnum, Type[AbstractDB]] = {
        DatabasesEnum.SQLITE: SqliteDB
        }
MODELS: Dict[ModelsEnum, Type[AbstractModel]] = {
        ModelsEnum.OPENAI: OpenAIModel
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
    default=Path(os.environ["HOME"]) / ".config/gpttui/database.sqlite",
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
    "--model_name",
    type=str,
    default="gpt-3.5-turbo",
    help="Model's name."
    )
@option(
    "--context",
    type=str,
    default="You are an AI assistant",
    help="Context for the model."
    )
def front(
    database_kind: DatabasesEnum,
    database_name: str,
    session: str,
    model_kind: ModelsEnum,
    model_name: str,
    context: str
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
    """
    db = (
            DBS[database_kind]()
            .setup(database=database_name)
            )
    db.create_session(session_name=session)
    model = (
            MODELS[model_kind]()
            .add_context(context=context)
            .setup(model_name=model_name, database=db, session_name=session)
            )
    app = (
            GptApp()
            .setup(model=model)
            )
    app.run()
