import os
import json
import requests
from google.cloud import dialogflow_v2 as dialogflow

DIALOGFLOW_PROJECT_ID = os.getenv('DIALOGFLOW_PROJECT_ID')
DIALOGFLOW_LANGUAGE_CODE = 'ja'
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

def detect_intent_texts(session_id, text):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    return response.query_result.fulfillment_text

def webhook(request):
    try:
        if request.method != 'POST':
            return 'Method Not Allowed', 405

        body = request.get_json(silent=True)
        print("BODY:", json.dumps(body, ensure_ascii=False))

        # イベントが無い or 空のときは400を返す
        if not body or 'events' not in body or len(body['events']) == 0:
            print("No events received.")
            return 'No events', 200

        event = body['events'][0]
        if event['type'] != 'message' or event['message']['type'] != 'text':
            return 'Event type not supported', 200  # 応答は200にするのがLINEの仕様
        reply_token = event['replyToken']
        user_message = event['message']['text']
        user_id = event['source']['userId']

        reply_text = detect_intent_texts(user_id, user_message)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}'
        }
        data = {
            'replyToken': reply_token,
            'messages': [{'type': 'text', 'text': reply_text}]
        }

        r = requests.post('https://api.line.me/v2/bot/message/reply',
                          headers=headers,
                          data=json.dumps(data))

        print("LINE response:", r.status_code, r.text)

        if r.status_code != 200:
            return f"Failed to reply: {r.text}", 500

        return 'OK', 200

    except Exception as e:
        print("Webhook Error:", e)
        return 'Internal Server Error', 500