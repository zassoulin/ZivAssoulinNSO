# manage SQLite database
import sqlite3


class SQLiteController:
    def __init__(self, db_host, db_port, db_path):
        self.db_host = db_host
        self.db_port = db_port
        self.db_path = db_path
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(f"sqlite://{self.db_host}:{self.db_port}/{self.db_path}")
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

    def init_database(self):
        self.connect()
        self.create_table("messages", "message_id TEXT PRIMARY KEY,application_id INTEGER NOT NULL,session_id TEXT "
                                      "NOT NULL,participants TEXT NOT NULL,content TEXT NOT NULL")
