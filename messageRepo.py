from message import Message


class MessageRepo:
    # class uses the SQliteController to store and retrieve messages
    # initialize the message repository
    def __init__(self, SQliteController):
        self.SQliteController = SQliteController
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
        message = self.SQliteController.select("messages", "*", f"application_id={application_id}")
        return Message.from_json(message[0]) if message else None

    def get_by_session_id(self, session_id):
        # get the message by session id
        message = self.SQliteController.select("messages", "*", f"session_id='{session_id}'")
        return Message.from_json(message[0]) if message else None

    def get_by_message_id(self, message_id):
        # get the message by message id
        message = self.SQliteController.select("messages", "*", f"message_id='{message_id}'")
        return Message.from_json(message[0]) if message else None
    def delete_by_message_id(self, message_id):
        self.SQliteController.delete("messages", f"message_id='{message_id}'")
    def delete_by_session_id(self, session_id):
        self.SQliteController.delete("messages", f"session_id='{session_id}'")
    def delete_by_application_id(self, application_id):
        self.SQliteController.delete("messages", f"application_id={application_id}")
