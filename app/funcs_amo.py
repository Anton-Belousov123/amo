import json
import time

import bs4
import requests

from app import auth


def get_pipeline(image, s_name, text):
    from app.auth import get_token
    token, session = get_token()
    url = 'https://kevgenev8.amocrm.ru/ajax/leads/multiple/loadmore/?skip_filter=Y'
    print(image, s_name, text)
    data = {
        'json': 'true',
        'page': 1,
        'ELEMENT_COUNT': 1000000,
        'pipeline': 'Y',
        'pipeline_id': 6731170
    }
    response = session.post(url, timeout=15, data=data).json()['items']

    for i in response['items']:
        img = i['source_data']['client']['picture']
        name = i['source_data']['client']['name']
        message = i['source_data'][0]['text']
        print(img, name, message)
        pipeline = i['id']
        print(img, name, message)
        if (img == image) or (message == text and s_name == name):
            return pipeline
    return None


def send_message(receiver_id: str, message: str, token, account_chat_id):
    headers = {'X-Auth-Token': token}
    url = f'https://amojo.amocrm.ru/v1/chats/{account_chat_id}/' \
          f'{receiver_id}/messages?with_video=true&stand=v15'
    requests.post(url, headers=headers, data=json.dumps({"text": message}))


def get_chat_history_try(receiver_id: str, token, account_chat_id):
    headers = {'X-Auth-Token': token}
    url = f'https://amojo.amocrm.ru/messages/{account_chat_id}/merge?stand=v15' \
          f'&offset=0&limit=100&chat_id%5B%5D={receiver_id}&get_tags=true&lang=ru'
    message_list = requests.get(url, headers=headers).json()
    return message_list['message_list']


def send_notes(pipeline_id, session, text):
    url = f'https://kevgenev8.amocrm.ru/private/notes/edit2.php?parent_element_id={pipeline_id}&parent_element_type=2'
    data = {
        'DATE_CREATE': int(time.time()),
        'ACTION': 'ADD_NOTE',
        'BODY': text,
        'ELEMENT_ID': pipeline_id,
        'ELEMENT_TYPE': '2'
    }
    resp = session.post(url, data=data)
    print(resp.text)


def get_chat_history(receiver_id, token, account_chat_id):
    while True:
        try:
            chat_history = get_chat_history_try(receiver_id, token, account_chat_id)
        except Exception as e:
            print(e, 1)
            token, _ = auth.get_token()
            continue
        break
    return token, chat_history
