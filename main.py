from flask import Flask, request, jsonify

from SQliteController import SQLiteController
from messageRepo import MessageRepo
from message import Message


class MessageServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.messageRepo = MessageRepo(SQLiteController("messages.db"))

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
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_message(self):
        try:
            param_type = request.args.get('param_type')
            param_value = request.args.get('param_value')

            if not param_type or not param_value:
                return jsonify({'error': 'Missing required parameters: param_type and/or param_value'}), 400

            res_message = None
            if param_type == 'applicationId':
                res_message = self.messageRepo.get_by_application_id(param_value)
            elif param_type == 'sessionId':
                res_message = self.messageRepo.get_by_session_id(param_value)
            elif param_type == 'messageId':
                res_message = self.messageRepo.get_by_message_id(param_value)

            return jsonify(res_message.to_json())
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def delete_message(self):
        try:
            param_type = request.args.get('param_type')
            param_value = request.args.get('param_value')

            if not param_type or not param_value:
                return jsonify({'error': 'Missing required parameters: param_type and/or param_value'}), 400

            if param_type == 'applicationId':
                self.messageRepo.delete_by_application_id(param_value)
            elif param_type == 'sessionId':
                self.messageRepo.delete_by_session_id(param_value)
            elif param_type == 'messageId':
                self.messageRepo.delete_by_message_id(param_value)

            return jsonify({'message': 'Messages deleted successfully'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    server = MessageServer()
    server.run()
