import json

import pytest
from flask import Flask
from message import Message
from messageServer import MessageServer

json_data = {
    'message_id': 'messageid_1',
    'application_id': 1,
    'session_id': 'sessionid_1',
    'participants': ['Ziv', 'Noam'],
    'content': 'hi'
}


class TestMessageServer:
    """Testing for this class can be done with 2 different ways unit testing or integration/E2E testing I summed the
    intention here is to do E2E testing, so I will use an in memory db with flask test client instead of mocking the
    messagesRepo"""

    def test_add_message_valid(self, message_server):
        response = message_server.app.test_client().post('/AddMessage', json=json_data)
        assert response.status_code == 201  # Expect HTTP status code 201 for success

    def test_get_message_by_application_id(self, message_server):
        message_server.app.test_client().post('/AddMessage', json=json_data)  # adding and getting a message
        response = message_server.app.test_client().get('/GetMessage?applicationId=1')
        assert response.status_code == 200, "received a fail status code"  # Expect HTTP status code 200 for success
        assert response.json['message'][0]['message_id'] == json_data['message_id'], "received a wrong message"

    def test_delete_message_by_application_id(self, message_server):
        message_server.app.test_client().post('/AddMessage', json=json_data)  # adding message
        response = message_server.app.test_client().delete('/DeleteMessage?applicationId=1')  # deleting message
        assert response.status_code == 200  # Expect HTTP status code 200 for success
        #verify that message was deleted
        response = message_server.app.test_client().get('/GetMessage?applicationId=1')
        assert response.json['message'] == [], "Error message was not deleted"
    def test_add_message_invalid(self, message_server):
        response = message_server.app.test_client().post('/AddMessage', json={})
        assert response.status_code == 400  # Expect HTTP status code 400 for bad request
    def test_add_existing_message(self, message_server):
        message_server.app.test_client().post('/AddMessage', json=json_data)
        response = message_server.app.test_client().post('/AddMessage', json=json_data)
        assert response.status_code == 400
