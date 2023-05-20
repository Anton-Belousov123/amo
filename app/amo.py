import asyncio
import json
import os
import time

from flask import Flask, request
import requests
import dotenv
from app import gpt, auth

dotenv.load_dotenv('misc/.env')

token = ''
app = Flask(__name__)
account_chat_id = os.getenv('ACCOUNT_CHAT_ID')
print(account_chat_id)
user_dict = {}


def send_message(receiver_id: str, message: str):
    print(message, 'answer')
    headers = {'X-Auth-Token': token}
    url = f'https://amojo.amocrm.ru/v1/chats/{account_chat_id}/' \
          f'{receiver_id}/messages?with_video=true&stand=v15'
    response = requests.post(url, headers=headers, data=json.dumps({"text": message}))
    print(response.text)

def get_chat_history(receiver_id: str):
    headers = {'X-Auth-Token': token}
    url = f'https://amojo.amocrm.ru/messages/{account_chat_id}/merge?stand=v15' \
          f'&offset=0&limit=100&chat_id%5B%5D={receiver_id}&get_tags=true&lang=ru'
    message_list = requests.get(url, headers=headers).json()
    print(message_list)
    return message_list['message_list']


@app.route('/webapp', methods=["POST"])
def webapp():
    global token
    d = request.form.to_dict()
    if int(d['message[add][0][created_at]']) + 10 < int(time.time()):
        return 'ok'
    receiver_id = d['message[add][0][chat_id]']
    print(receiver_id, 'rec-id')


def translate_it(m):
    print('yes translate me')

@app.route('/', methods=["POST"])
def hello():
    global token
    d = request.form.to_dict()
    if int(d['message[add][0][created_at]']) + 10 < int(time.time()):
        return 'ok'
    receiver_id = d['message[add][0][chat_id]']
    print(d)
    if d['message[add][0][text]'] == 'Зарегистрироваться в WebApp':
        return 'ok'


    while True:
        try:
            chat_history = get_chat_history(receiver_id)
        except Exception as e:
            print(e, 1)
            token = auth.get_token()
            continue
        break
    fl = False
    alphabet = ['А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т',
                'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ъ', 'Ы', 'Ь', 'Э', 'Ю', 'Я', 'а', 'б', 'в', 'г', 'д', 'е', 'ё',
                'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ',
                'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    for s in d['message[add][0][text]']:
        if s in alphabet: fl = True
    if not fl:
        translate_it(d['message[add][0][text]'])
    prepared_request, limit = gpt.prepare_request(chat_history)
    message = gpt.get_answer(prepared_request, limit)
    while True:
        try:
            send_message(receiver_id, message)
        except Exception as e:
            print(e, 2)
            token = auth.get_token()
            continue
        break


    fl = False
    for s in message:
        if s in alphabet: fl = True
    if not fl:
        translate_it(message)


    return 'ok'


app.run(host='0.0.0.0', debug=True, port=8000)
