import sqlite3
from gpttui.database.base import AbstractDB, Message, Messages
from typing import Callable, List


class SqliteDB(AbstractDB):
    connection: sqlite3.Connection

    def setup(self, **kwargs: str) -> "AbstractDB":
        self.connection = sqlite3.connect(kwargs["database"])
        return self

    def __write_with_connection(self, f: Callable):
        cursor = self.connection.cursor()
        f(cursor)
        self.connection.commit()

    def __read_with_connection(self, f: Callable) -> List:
        cursor = self.connection.cursor()
        f(cursor)
        result = list(cursor.fetchall())
        return result

    def create_session(self, session_name: str):
        f = lambda cursor: cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {session_name}(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    role TEXT,
                    content TEXT,
                    date TEXT
                    );
                """
                )
        self.__write_with_connection(f)

    def delete_session(self, session_name: str):
        f = lambda cursor: cursor.execute(
                f"""
                DROP TABLE {session_name};
                """
                )
        self.__write_with_connection(f)

    def add_message(self, msg: Message, session_name: str):
        return super().add_message(msg, session_name)

    def get_messages(self, query: str, session_name: str) -> Messages:
        return super().get_messages(query, session_name)

    def close(self):
        return super().close()
