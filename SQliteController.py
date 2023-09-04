# manage SQLite database
import os
import sqlite3


class SQLiteController:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(f"{self.db_path}")
            print("Connected to the database")
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")

    def disconnect(self):
        try:
            self.conn.close()
            print("Disconnected from the database")
        except sqlite3.Error as e:
            print(f"Error disconnecting from the database: {e}")

    def create_table(self, table_name, columns):
        try:
            self.conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")
            print(f"Table {table_name} created")
        except sqlite3.Error as e:
            print(f"Error creating table {table_name}: {e}")
    def insert(self, table_name, record):
        try:
            self.conn.execute(f"INSERT INTO {table_name} VALUES {record}")
            self.conn.commit()
            print(f"Record {record} inserted into table {table_name}")
        except sqlite3.Error as e:
            print(f"Error inserting record {record} into table {table_name}: {e}")
    def select(self, table_name, columns="*", condition=None):
        try:
            cursor = self.conn.cursor()
            query = f"SELECT {columns} FROM {table_name}"
            if condition:
                query += f" WHERE {condition}"
            cursor.execute(query)
            data = cursor.fetchall()
            return data
        except sqlite3.Error as e:
            print(f"Error executing select query: {e}")
            return None
    #add delete method
    def delete(self, table_name, condition=None):
        try:
            cursor = self.conn.cursor()
            query = f"DELETE FROM {table_name}"
            if condition:
                query += f" WHERE {condition}"
            cursor.execute(query)
            self.conn.commit()
            print(f"Record deleted from table {table_name}")
        except sqlite3.Error as e:
            print(f"Error executing delete query: {e}")
            return None
