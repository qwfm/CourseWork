import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.zoom_rest import ZoomREST
from src.zoom_chat import ZoomChat

app = Flask(__name__)
CORS(app)

zoom_rest = ZoomREST()
zoom_chat = ZoomChat()

@app.route('/api/meetings', methods=['POST'])
def create_meeting():
    data = request.get_json()
    m = zoom_rest.create_meeting(
        data['topic'], data['start_time'], data['duration']
    )
    return jsonify(m)

@app.route('/api/meetings', methods=['GET'])
def list_meetings():
    return jsonify({"meetings": zoom_rest.get_meetings()})

@app.route('/api/meetings/<int:mid>', methods=['DELETE'])
def delete_meeting(mid):
    ok = zoom_rest.delete_meeting(mid)
    return ('', 204) if ok else ('', 500)

@app.route('/api/chat', methods=['POST'])
def send_chat():
    data = request.get_json()
    resp = zoom_chat.send_message(data['to'], data['message'])
    return jsonify(resp)

@app.route('/api/channels', methods=['GET'])
def get_channels():
    try:
        channels = zoom_chat.get_channels()
        return jsonify({"channels": channels})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    