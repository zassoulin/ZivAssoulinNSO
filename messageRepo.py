from SQliteController import SQLiteController
from message import Message


class MessageRepo:
    # class uses the SQliteController to store and retrieve messages
    # initialize the message repository
    def __init__(self, SQLiteController):
        self.SQliteController = SQLiteController
        self.init_database()

    def init_database(self):
        # create the messages table if it does not exist
        self.SQliteController.create_table("messages",
                                           "message_id TEXT PRIMARY KEY,application_id INTEGER NOT NULL,session_id TEXT "
                                           "NOT NULL,participants TEXT NOT NULL,content TEXT NOT NULL")

    def insert(self, message: Message):
        # insert the message into the database
        self.SQliteController.insert("messages", message.to_json())

    # creating 3 different methods instead of one with optional parameters to make the code more readable
    def get_by_application_id(self, application_id):
        # get the message by application id
        message_data, field_names = self.SQliteController.select("messages", "*", f"application_id={application_id}")
        if message_data is None:
            return None
        return self.create_message_from_values_and_fields_names(message_data[0], field_names)

    def get_by_session_id(self, session_id):
        # get the message by session id
        message_data, field_names = self.SQliteController.select("messages", "*", f"session_id='{session_id}'")
        if message_data is None:
            return None
        return self.create_message_from_values_and_fields_names(message_data[0], field_names)

    def get_by_message_id(self, message_id):
        # get the message by message id
        message_data, field_names = self.SQliteController.select("messages", "*", f"message_id='{message_id}'")
        if message_data is None:
            return None
        return self.create_message_from_values_and_fields_names(message_data[0],field_names)

    def delete_by_message_id(self, message_id):
        self.SQliteController.delete("messages", f"message_id='{message_id}'")

    def delete_by_session_id(self, session_id):
        self.SQliteController.delete("messages", f"session_id='{session_id}'")

    def delete_by_application_id(self, application_id):
        self.SQliteController.delete("messages", f"application_id={application_id}")

    def create_message_from_values_and_fields_names(self, values, field_names):
        """creates a message from values and field names inorder to make the order of the values irrelevant"""
        message = Message(values[field_names.index("message_id")],
                          values[field_names.index("application_id")],
                          values[field_names.index("session_id")],
                          values[field_names.index("participants")],
                          values[field_names.index("content")])
        return message


if __name__ == '__main__':
    sqls = SQLiteController("test.db")
    sqls.connect()
    MessageRepo = MessageRepo(sqls)
    MessageRepo.insert(Message("5", 5, "4", [1, 2], "5"))
    print(MessageRepo.get_by_message_id(5))
    sqls.disconnect()
