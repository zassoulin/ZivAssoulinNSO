# Message Server Flask App

This Flask app, **MessageServer**, is responsible for handling requests to a message database. It allows users to add, retrieve, and delete messages from the database.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/zassoulin/ZivAssoulinNSO.git
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   python message_server.py
   ```

The server will be running by default on `http://localhost:5000`.
this can be changed in the `message_server.py` main.

## Usage

### Add a Message

To add a message to the database, send a POST request to `/AddMessage` with a JSON body containing the message details.

Example:
```bash
curl -X POST -H "Content-Type: application/json" -d '{
    "message_id": "messageid_1",
    "application_id": 1,
    "session_id": "sessionid_1",
    "participants": ["Ziv", "Noam"],
    "content": "hi"
}' http://localhost:5000/AddMessage
```

### Get Messages

To retrieve messages from the database, send a GET request to `/GetMessage` with query parameters to filter the results. You can filter by `applicationId`, `sessionId`, or `messageId`.

Example:
```bash
# Get messages by applicationId
curl http://localhost:5000/GetMessage?applicationId=1

# Get messages by sessionId
curl http://localhost:5000/GetMessage?sessionId=sessionid_1

# Get messages by messageId
curl http://localhost:5000/GetMessage?messageId=messageid_1
```

### Delete a Message

To delete a message from the database, send a DELETE request to `/DeleteMessage` with query parameters to specify which message to delete. You can delete by `applicationId`, `sessionId`, or `messageId`.

Example:
```bash
# Delete a message by applicationId
curl -X DELETE http://localhost:5000/DeleteMessage?applicationId=1

# Delete a message by sessionId
curl -X DELETE http://localhost:5000/DeleteMessage?sessionId=sessionid_1

# Delete a message by messageId
curl -X DELETE http://localhost:5000/DeleteMessage?messageId=messageid_1
```

## Error Handling

- Missing required fields when adding a message will result in a 400 Bad Request response.
- Deleting a non-existing message will result in a 404 Not Found response.
- Other server errors will result in a 500 Internal Server Error response.

## Dependencies

- Flask: A micro web framework for Python.
- pytest: A framework for building simple and scalable tests.
