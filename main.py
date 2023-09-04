from flask import Flask


if __name__ == '__main__':
    app = Flask(__name__)
    app.run(debug=True)

#build a flask service to handle the request POST / AddMessage
def add_message():
    pass
#build a flask service to handle the request GET / GetMessages
#build a flask service to handle the request GET / GetMessageById
#build a flask service to handle the request PUT / UpdateMessage
#build a flask service to handle the request DELETE / DeleteMessage
