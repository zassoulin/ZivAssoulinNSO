import sqlite3
import pytest

from SQLException import SQLException
from SQliteController import SQLiteController


class TestSQLiteController:
    # Define class variables for table name and columns
    TEST_TABLE_NAME = "test_users_table"
    TEST_TABLE_COLUMNS = "id INTEGER PRIMARY KEY, name TEXT"

    def test_create_table(self, sqlite_controller):
        sqlite_controller.create_table(self.TEST_TABLE_NAME, self.TEST_TABLE_COLUMNS)  # can be extracted to a fixture

        cursor = sqlite_controller.conn.cursor()
        cursor.execute(
            f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.TEST_TABLE_NAME}'")  # search for the table name in the database metadata
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == self.TEST_TABLE_NAME

    def test_insert_and_select(self, sqlite_controller):
        sqlite_controller.create_table(self.TEST_TABLE_NAME, self.TEST_TABLE_COLUMNS)

        record = {"name": "ziv"}
        sqlite_controller.insert(self.TEST_TABLE_NAME, record)

        data, field_names = sqlite_controller.select(self.TEST_TABLE_NAME)
        assert len(data) == 1
        assert len(field_names) == 2
        assert field_names == ["id", "name"]
        assert data[0][1] == "ziv"
        assert data[0][0] == 1

    def test_delete(self, sqlite_controller):
        # Use the class variables for table name and columns
        sqlite_controller.create_table(self.TEST_TABLE_NAME, self.TEST_TABLE_COLUMNS)

        records = [{"name": "ziv"}, {"name": "noam"}]
        for record in records:
            sqlite_controller.insert(self.TEST_TABLE_NAME, record)

        sqlite_controller.delete(self.TEST_TABLE_NAME, "name = 'noam'")

        data, field_names = sqlite_controller.select(self.TEST_TABLE_NAME)
        assert len(data) == 1
        assert len(field_names) == 2
        assert field_names == ["id", "name"]
        assert set(data) == {(1, "ziv")}

    def test_execute_invalid_sql_query(self, sqlite_controller):
        with pytest.raises(SQLException):  # test for invalid sql query
            sqlite_controller.select("invalid_table")
