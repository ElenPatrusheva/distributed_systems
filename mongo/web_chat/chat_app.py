import pymongo
from flask import Flask, request, render_template
import os

app = Flask(__name__)
client = pymongo.MongoClient(os.environ['MONGO'])
db = client.chat_db

while True:
    try:
        client.admin.command('ismaster')
    except ConnectionFailure:
        pass
    else:
        break

def list_messages():
    collection = db['messages']
    messages = collection.find({}, {'_id': 0})
    return messages

@app.route('/', methods=['POST'])
def get_form():
    message = request.form['Message']
    author = request.form['Sender']

    collection = db.messages
    collection.insert_one({'sender': author, 'message': message})
    return render_template('index.html', messages=list_messages())

@app.route('/')
def main_page():
    return render_template('index.html', messages=list_messages())


if __name__ == '__main__':
    app.run()
