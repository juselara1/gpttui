"""
This file defines the required elements to use sqlite as a database.
"""
import sqlite3
from gpttui.database.base import AbstractDB, MessageWithTime, Messages, Message
from typing import Callable, List

class SqliteDB(AbstractDB):
    """
    This class represents a database based on SQLITE.

    Attributes
    ----------
    connection : sqlite3.Connection
        Connection with a sqlite database.
    """
    connection: sqlite3.Connection

    def setup(self, **kwargs: str) -> "AbstractDB":
        """
        This method allows creating a connection with the database.

        Parameters
        ----------
        database : str
            Database filename.

        Returns
        -------
        AbstractDB
            Instance of the database.
        """
        self.connection = sqlite3.connect(kwargs["database"])
        return self

    def __write_with_connection(self, f: Callable):
        """
        This method is used to handle the sqlite cursor object for write operations.

        Parameters
        ----------
        f : Callable
            Function with a query that must be executed.
        """
        cursor = self.connection.cursor()
        f(cursor)
        self.connection.commit()

    def __read_with_connection(self, f: Callable) -> List:
        """
        This method is used to handle the sqlite cursor object for read operations.

        Parameters
        ----------
        f : Callable
            Function with a query that must be executed.
        """
        cursor = self.connection.cursor()
        f(cursor)
        result = list(cursor.fetchall())
        return result

    def create_session(self, session_name: str):
        """
        Creates a session (table) in sqlite.

        Parameters
        ----------
        session_name : str
            Session name.
        """
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
        """
        Deletes a session (table) in sqlite.
        
        Parameters
        ----------
        session_name : str
            Session name.
        """
        f = lambda cursor: cursor.execute(
                f"""
                DROP TABLE {session_name};
                """
                )
        self.__write_with_connection(f)

    def add_message(self, msg: MessageWithTime, session_name: str):
        """
        Saves a message (row) in the database.

        Parameters
        ----------
        msg : MessageWithTime
            Message to store.
        session_name : str
            Session name.
        """
        f = lambda cursor: cursor.execute(
                f"""
                INSERT INTO {session_name} (
                    role, content, timestamp
                    )
                VALUES (?, ?, ?);
                """,
                (msg.message.role, msg.message.content, msg.timestamp)
                )
        self.__write_with_connection(f)

    def get_messages(self, session_name: str) -> Messages:
        """
        Extracts the most recent messages from the database.

        Parameters
        ----------
        session_name : str
            Session name.
        """
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
        """
        Closes the connection with the database.
        """
        self.connection.close()
