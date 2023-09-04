import pytest

from SQLException import SQLException
from message import Message

test_message1 = Message("message1", 1, "session1", ["Ziv", "Noam"], "Hello")


class TestMessageRepo:  # ideal unit test will use mocking instead of real database(even if it is in memory)
    def test_insert_and_get_by_application_id(self, message_repo):
        message_repo.insert(test_message1)
        messages = message_repo.get_by_application_id(1)
        assert len(messages) == 1
        assert messages[0] == test_message1

    def test_insert_and_get_by_session_id(self, message_repo):
        message_repo.insert(test_message1)
        messages = message_repo.get_by_session_id("session1")
        assert len(messages) == 1
        assert messages[0] == test_message1

    def test_insert_and_get_by_message_id(self, message_repo):
        message_repo.insert(test_message1)
        messages = message_repo.get_by_message_id("message1")
        assert len(messages) == 1
        assert messages[0] == test_message1

    def test_delete_by_message_id(self, message_repo):
        message_repo.insert(test_message1)
        message_repo.delete_by_message_id("message1")
        messages = message_repo.get_by_application_id(1)
        assert len(messages) == 0

    def test_delete_by_session_id(self, message_repo):
        message_repo.insert(test_message1)
        message_repo.delete_by_session_id("session1")
        messages = message_repo.get_by_session_id("session1")
        assert len(messages) == 0

    def test_delete_by_application_id(self, message_repo):
        message_repo.insert(test_message1)
        message_repo.delete_by_application_id(1)
        messages = message_repo.get_by_application_id(1)
        assert len(messages) == 0

    def test_insert_duplicate(self, message_repo):
        message_repo.insert(test_message1)
        with pytest.raises(SQLException):
            message_repo.insert(test_message1)  # verify that duplicate message id cannot be inserted, not checking
            # all unique fields manually
