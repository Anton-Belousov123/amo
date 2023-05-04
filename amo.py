import json
from flask import Flask, request
import requests

import gpt

app = Flask(__name__)
account_chat_id = '7eb31c63-e74d-41cd-86f7-34c6265386f9'
headers = {'X-Auth-Token': '19998763-dfbf-4b85-9f1e-a49315e5d2f0'}
my_id = '9389b299-c47b-4607-aad1-3a7baa307bbd'


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
    d = request.form.to_dict()
    receiver_id = d['message[add][0][chat_id]']
    chat_history = get_chat_history(receiver_id)
    prepared_request = gpt.prepare_request(chat_history)
    message = gpt.get_answer(prepared_request)
    send_message(receiver_id, message)
    return 'ok'


app.run(host='0.0.0.0', debug=True, port=80)

