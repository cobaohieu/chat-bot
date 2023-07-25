from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import requests

app = Flask(__name__,template_folder='templates')
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('default.html')

@socketio.on('message')
def handle_message(data):
    url = 'https://api.openai.com/v4/engines/davinci-codex/completions'
    headers = {
        'Authorization': 'Your API Key',
        'Content-Type': 'application/json'
    }
    post_data = {
        'prompt': data,
        'max_tokens': 60
    }
    response = requests.post(url, headers=headers, json=post_data)
    message = response.json()['choices'][0]['text'].strip()
    emit('message', {'text': message}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=88888, debug=True)  # Run the Flask app in debug mode for development purposes
