from flask import Flask, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
messages = {}

@app.route('/log', methods=['POST', 'GET'])
def handle_requests():
    if request.method == 'POST':
        data = request.json
        uuid = data['uuid']
        msg = data['msg']
        messages[uuid] = msg
        print(f"Received message: {msg}")
        return "Message status: logged"
    elif request.method == 'GET':
        return "\n".join(messages.values())

if __name__ == '__main__':
    app.run(port=5001)
