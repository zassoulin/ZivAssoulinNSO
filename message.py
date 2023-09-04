class Message:
    # domain object for message
    def __init__(self, message_id, application_id, session_id, participants, content):
        self.message_id = message_id
        self.application_id = application_id
        self.session_id = session_id
        self.participants = participants
        self.content = content

    def __str__(self):
        return f"Message: {self.message_id},{self.application_id},{self.session_id},{self.participants},{self.content}"

    def to_json(self):
        return {"message_id": self.message_id, "application_id": self.application_id, "session_id": self.session_id,
                "participants": self.participants, "content": self.content}

    def from_json(self, json: dict):
        self.message_id = json["message_id"]
        self.application_id = json["application_id"]
        self.session_id = json["session_id"]
        self.participants = json["participants"]
        self.content = json["content"]
        return self
