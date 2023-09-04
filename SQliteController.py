# manage SQLite database
import os
import sqlite3

from SQLException import SQLException


class SQLiteController:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(f"{self.db_path}" , check_same_thread=False)#flask runs by defualt on multiple threads,in sqlite3 when running on multiple threads race conditions may occur when trying to insert
            # data into the database with same unique Id, there are a couple of ways to solve this such as running
            # flask on single thread,creating a sql connection on each request or setting check_same_thread=False
            # prevents this from happening(there are other possible solutions) I have chosen the last option as
            # usually in databases it is a best practice to keep 1 connection alive for the entire application.
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
            raise SQLException(f"Error creating table {table_name}")

    def insert(self, table_name, record):
        try:
            columns = ', '.join(record.keys())
            placeholders = ', '.join(['?'] * len(record))
            values = tuple(record.values())

            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            self.conn.execute(query, values)
            self.conn.commit()
            print(f"Record inserted into table {table_name}")
        except sqlite3.IntegrityError as e:
            raise SQLException(f"Error inserting record into table invalid data unique id already exists")
        except sqlite3.Error as e:
            raise SQLException(f"Error executing insert query")

    def select(self, table_name, columns="*", condition=None):
        try:
            cursor = self.conn.cursor()
            query = f"SELECT {columns} FROM {table_name}"
            if condition:
                query += f" WHERE {condition}"
            cursor.execute(query)
            data = cursor.fetchall()
            field_names = [desc[0] for desc in cursor.description]
            return data , field_names
        except sqlite3.Error as e:
            raise SQLException(f"Error executing select query")

    # add delete method
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
            raise SQLException(f"Error executing delete query")
