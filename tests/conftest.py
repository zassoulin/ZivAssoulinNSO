import sqlite3
import pytest
from SQliteController import SQLiteController
from messageRepo import MessageRepo


# Define SQLiteController fixture
@pytest.fixture
def sqlite_controller():
    conn = sqlite3.connect(":memory:")
    controller = SQLiteController(":memory:")
    controller.connect()
    yield controller
    controller.disconnect()
    conn.close()

# Define MessageRepo fixture
@pytest.fixture
def message_repo(sqlite_controller):
    return MessageRepo(sqlite_controller)
