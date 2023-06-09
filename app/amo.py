import json
import os
import time

import requests
from flask import Flask, request
import dotenv
from app import gpt, auth, deepl
from app.funcs_amo import get_pipeline, get_chat_history, send_notes

dotenv.load_dotenv('misc/.env')
token = ''
app = Flask(__name__)
account_chat_id = os.getenv('ACCOUNT_CHAT_ID')


def send_message(receiver_id: str, message: str):
    headers = {'X-Auth-Token': token}
    url = f'https://amojo.amocrm.ru/v1/chats/{account_chat_id}/' \
          f'{receiver_id}/messages?with_video=true&stand=v15'
    response = requests.post(url, headers=headers, data=json.dumps({"text": message}))


@app.route('/', methods=["POST"])
def hello():
    global token
    d = request.form.to_dict()
    print('Новое сообщение!')
    try:
        image = d['message[add][0][author][avatar_url]']
    except:
        image = ''
    name = d['message[add][0][author][name]']
    text = d['message[add][0][text]']
    pipeline = get_pipeline(image, name, text)
    if pipeline is None or int(d['message[add][0][created_at]']) + 10 < int(time.time()) or d[
        'message[add][0][text]'] == 'Зарегистрироваться в WebApp':
        print('Не удалось идентифицировать пользователя!')
        return 'ok'
    print('Пользователь идентифицирован!')
    receiver_id = d['message[add][0][chat_id]']
    token, chat_history = get_chat_history(receiver_id, token, account_chat_id)
    print("История сообщений получена!")
    # lang, text = deepl.translate_it(str(chat_history), 'EN')
    # print('История сообщений переведена!')
    # print(text)
    # return

    token, session = auth.get_token()
    send_notes(pipeline, session, (deepl.translate_it(chat_history[0]['text'], 'RU'))[1])
    print('Исходное сообщение переведено!')

    prepared_request, limit = gpt.prepare_request(chat_history)

    message = gpt.get_answer(prepared_request, limit)

    while True:
        try:
            send_message(receiver_id, message)
        except Exception as e:
            print(e, 2)
            token, session = auth.get_token()
            continue
        break

    send_notes(pipeline, session, (deepl.translate_it(message, 'RU'))[1])
    return 'ok'


app.run(host='0.0.0.0', debug=True, port=8000)
