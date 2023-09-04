import sqlite3
import pytest
from flask import Flask

from SQliteController import SQLiteController
from messageServer import MessageServer
from messageRepo import MessageRepo


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

@pytest.fixture
def message_server(sqlite_controller):
    server = MessageServer(sqlite_controller)
    yield server
