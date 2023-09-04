from flask import Flask, request, jsonify

from SQLException import SQLException
from SQliteController import SQLiteController
from messageRepo import MessageRepo
from message import Message


class MessageServer:
    def __init__(self, sqliteController = None):
        self.app = Flask(__name__)
        if sqliteController is None:
            self.sqliteController = SQLiteController("messages.db")
        else:
            self.sqliteController = sqliteController
        self.sqliteController.connect()
        self.messageRepo = MessageRepo(self.sqliteController)

        # Define routes
        self.app.route('/AddMessage', methods=['POST'])(self.add_message)
        self.app.route('/GetMessage', methods=['GET'])(self.get_message)
        self.app.route('/DeleteMessage', methods=['DELETE'])(self.delete_message)

    def run(self, host='0.0.0.0', port=5000):
        self.app.run(host=host, port=port)

    def add_message(self):
        try:
            data = request.get_json()

            # Validate required fields
            required_fields = ['application_id', 'session_id', 'message_id', 'participants', 'content']
            for field in required_fields:
                if field not in data:
                    return jsonify({'error': f'Missing required field: {field}'}), 400
            # insert message into database
            message = Message(data['message_id'], data['application_id'], data['session_id'], data['participants'],
                              data['content'])
            self.messageRepo.insert(message)
            return jsonify({'message': 'Message added successfully'}), 201
        except SQLException as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify(
                {'error': 'Internal Server error'}), 500  # return 500 for any other exception with no debug info

    def get_message(self):
        try:
            if len(request.args) == 0:
                return jsonify({'error': 'Missing required parameters: param_type and/or param_value'}), 400
            elif len(request.args) != 1:
                return jsonify({'error': 'Too many parameters'}), 400

            res_messages = None
            if request.args.get('applicationId') is not None:
                res_messages = self.messageRepo.get_by_application_id(request.args.get('applicationId'))
            elif request.args.get('sessionId') is not None:
                res_messages = self.messageRepo.get_by_session_id(request.args.get('sessionId'))
            elif request.args.get('messageId') is not None:
                res_messages = self.messageRepo.get_by_message_id(request.args.get('messageId'))
            if res_messages is None:
                return jsonify({'error': 'Message not found'}), 404
            return jsonify({'message': [res_message.to_json() for res_message in res_messages]})
        except SQLException as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify(
                {'error': 'Internal Server error'}), 500  # return 500 for any other exception with no debug info

    def delete_message(self):
        try:
            if len(request.args) == 0:
                return jsonify({'error': 'Missing required parameters: param_type and/or param_value'}), 400
            elif len(request.args) != 1:
                return jsonify({'error': 'Too many parameters'}), 400

            res_message = None
            if request.args.get('applicationId') is not None:
                self.messageRepo.delete_by_application_id(request.args.get('applicationId'))
            elif request.args.get('sessionId') is not None:
                self.messageRepo.delete_by_session_id(request.args.get('sessionId'))
            elif request.args.get('messageId') is not None:
                self.messageRepo.delete_by_message_id(request.args.get('messageId'))

            return jsonify({'message': 'Messages deleted successfully'})
        except SQLException as e:
            return jsonify({'error': str(e)}), 400
        except Exception:
            return jsonify(
                {'error': 'Internal Server error'}), 500  # return 500 for any other exception with no debug info

    def __del__(self):
        self.sqliteController.disconnect()


if __name__ == '__main__':
    server = MessageServer()
    server.run()
