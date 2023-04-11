"""
Tests for the databases integration.
"""
import pytest, time
from gpttui.database.sqlite import SqliteDB
from gpttui.database.base import AbstractDB, Message, MessageWithTime

class TestSqliteDB:
    """
    Unittests for the sqlite database.
    """
    @staticmethod
    def setup_db() -> AbstractDB:
        """
        Initializes the database.

        Returns
        -------
        AbstractDB
            Initialized database.
        """
        db = SqliteDB().setup(database="test.db")
        return db

    @pytest.mark.parametrize("session_name", [f"chat{i}" for i in range(10)])
    def test_session(self, session_name: str):
        """
        Tests the session creation and deletion.

        Parameters
        ----------
        session_name : str
            Session name.
        """
        db = TestSqliteDB.setup_db()
        db.create_session(session_name)
        cursor = db.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_schema;")
        *result, = map(lambda i: i[0], cursor.fetchall())
        assert session_name in result

        db.delete_session(session_name)

        cursor = db.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_schema;")
        *result, = map(lambda i: i[0], cursor.fetchall())
        assert session_name not in result

    @pytest.mark.parametrize("message", ["hello", "testing", "hi"])
    def test_message(self, message: str):
        """
        Tests the save and retrieval of messages.

        Parameters
        ----------
        message : str
            Message to save.
        """
        db = TestSqliteDB.setup_db()
        db.create_session("test")
        msg = Message(role="user", content=message)
        msgt = MessageWithTime(message=msg, timestamp=int(time.time()))
        db.add_message(msgt, "test")

        messages = db.get_messages("test")
        msgt2 = messages.values[0].dict()
        assert msgt2 == msg.dict()
        db.delete_session("test")
