import json
class Message:
    # domain object for message
    def __init__(self, message_id, application_id, session_id, participants, content):
        self.message_id = message_id
        self.application_id = application_id
        self.session_id = session_id
        self.participants : list = participants
        self.content = content

    def __str__(self):
        return f'message_id: {self.message_id}, application_id: {self.application_id}, session_id: {self.session_id}, ' \
               f'participants: {self.participants}, content: {self.content}'

    def to_json(self):
        return {"message_id": self.message_id, "application_id": self.application_id, "session_id": self.session_id,
                "participants": json.dumps(self.participants) , "content": self.content}

    def from_json(self, json_data: dict):
        self.message_id = json_data["message_id"]
        self.application_id = json_data["application_id"]
        self.session_id = json_data["session_id"]
        self.participants = json.loads(json_data["participants"])
        self.content = json_data["content"]
        return self
    def __eq__(self, other):
        return self.message_id == other.message_id and self.application_id == other.application_id and self.session_id == other.session_id and self.participants == other.participants and self.content == other.content
