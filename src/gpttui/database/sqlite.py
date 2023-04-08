import sqlite3
from gpttui.database.base import AbstractDB, MessageWithTime, Messages, Message
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
                    timestamp INT
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

    def add_message(self, msg: MessageWithTime, session_name: str):
        f = lambda cursor: cursor.execute(
                f"""
                INSERT INTO {session_name} (
                    role, content, timestamp
                    )
                VALUES (
                    '{msg.message.role}', '{msg.message.content}', {msg.timestamp}
                    );
                """
                )
        self.__write_with_connection(f)

    def get_messages(self, session_name: str) -> Messages:
        f = lambda cursor: cursor.execute(
                f"""
                SELECT
                    role, content
                FROM
                    {session_name}
                ORDER BY
                    timestamp ASC
                ;
                """
                )
        result = self.__read_with_connection(f)
        messages = Messages(values=[Message(role=x[0], content=x[1]) for x in result])
        return messages

    def close(self):
        self.connection.close()
