import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.zoom_rest import ZoomREST
from src.zoom_chat import ZoomChat
import logging

logging.basicConfig(
    level=logging.DEBUG, 
    format='[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
)
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
    
@app.route('/zoom/webhook', methods=['POST'])
def zoom_webhook():
    data = request.get_json(force=True)
    app.logger.debug(f"Отримано webhook від Zoom: {data}")

    if not data:
        return 'Bad Request', 400

    if 'challenge' in data:
        return jsonify({'challenge': data['challenge']}), 200

    event = data.get('event')
    payload_obj = data.get('payload', {}).get('object', {})

    if event == "meeting.created":
        meeting_id = payload_obj.get('id')
        topic = payload_obj.get('topic')
        app.logger.info(f"Створено нову зустріч: {topic} (ID: {meeting_id})")

    elif event == "meeting.started":
        meeting_id = payload_obj.get('id')
        topic = payload_obj.get('topic')
        try:
            zoom_chat.send_message(
                to_jid="2d6fa43ed0ac4a228b997134f8a63407@conference.xmpp.zoom.us",
                message=f"Зустріч «{topic}» (ID: {meeting_id}) щойно почалася!"
            )
            app.logger.info(f"Надіслано повідомлення про початок зустрічі {meeting_id}")
        except Exception as e:
            app.logger.error(f"Не вдалося надіслати повідомлення: {e}")

    elif event == "chat_message.received":
        msg = payload_obj.get('message', {})
        sender = msg.get('sender', {})
        text = msg.get('message_content')
        user_name = sender.get('user_name') or sender.get('name')
        app.logger.info(f"Нове повідомлення від {user_name}: {text}")

    elif event == "team_chat.channel_message_posted":
        channel_name = payload_obj.get('channel_name')
        message = payload_obj.get('message')
        app.logger.info(f"Нове повідомлення в командному чаті каналу '{channel_name}': {message}")

    elif event == "chat_message.sent":
        channel_name = payload_obj.get('channel_name')
        message = payload_obj.get('message')
        app.logger.info(f"Повідомлення відправлено в канал '{channel_name}': {message}")

    else:
        app.logger.warning(f"Отримано невідому подію webhook: {event}")

    return '', 200


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    