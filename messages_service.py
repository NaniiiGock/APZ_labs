from flask import Flask
app = Flask(__name__)

from flask_cors import CORS
CORS(app)


@app.route('/messages')
def return_static_message():
    return 'waiting for implementation...'

if __name__ == '__main__':
    app.run(port=5002)
