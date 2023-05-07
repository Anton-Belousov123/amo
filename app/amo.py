import asyncio
import json
import os

from flask import Flask, request
import requests
import dotenv
from app import gpt, auth

dotenv.load_dotenv()

token = ''
app = Flask(__name__)
account_chat_id = os.getenv('ACCOUNT_CHAT_ID')
headers = {'X-Auth-Token': token}
used_message_ids = []

def send_message(receiver_id: str, message: str):
    url = f'https://amojo.amocrm.ru/v1/chats/{account_chat_id}/' \
          f'{receiver_id}/messages?with_video=true&stand=v15'
    requests.post(url, headers=headers, data=json.dumps({"text": message}))


def get_chat_history(receiver_id: str):
    url = f'https://amojo.amocrm.ru/messages/{account_chat_id}/merge?stand=v15' \
          f'&offset=0&limit=100&chat_id%5B%5D={receiver_id}&get_tags=true&lang=ru'
    message_list = requests.get(url, headers=headers).json()['message_list']
    return message_list


@app.route('/', methods=["POST"])
def hello():
    global token
    d = request.form.to_dict()
    if d['message[add][0][id]'] in used_message_ids:
        return 'ok'
    used_message_ids.append(d['message[add][0][id]'])
    print(d)
    receiver_id = d['message[add][0][chat_id]']
    while True:
        try:
            chat_history = get_chat_history(receiver_id)
        except Exception as e:
            print(e, 1)
            token = auth.get_token()
            continue
        break
    prepared_request = gpt.prepare_request(chat_history)
    message = gpt.get_answer(prepared_request)

    while True:
        try:
            send_message(receiver_id, message)
        except Exception as e:
            print(e, 2)
            token = auth.get_token()
            continue
        break
    return 'ok'


app.run(host='0.0.0.0', debug=True, port=8000)
