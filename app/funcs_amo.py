import json
import time

import bs4
import requests

from app import auth


def get_pipeline(image, s_name, text):
    from app.auth import get_token
    token, session = get_token()
    url = 'https://kevgenev8.amocrm.ru/leads/pipeline/6731170/?skip_filter=Y'
    print(image, s_name, text)
    response = session.get(url, timeout=15)
    soup = bs4.BeautifulSoup(response.text, features='html.parser')
    for i in soup.find_all('div', {'class': 'pipeline-unsorted__item-data'}):
        img = i.find('div', {'class': 'pipeline-unsorted__item-avatar'}). \
            get('style').replace("background-image: url(", '').replace(')', '')

        name = i.find('a', {'class': 'pipeline-unsorted__item-title'}).text
        message = i.find('div', {'class': 'pipeline_leads__linked-entities_last-message__text'}).text
        pipeline = i.find('a', {'class': 'pipeline-unsorted__item-title'}).get('href').split('/')[-1]
        if (img == image) or (message == text and s_name == name):
            return pipeline
    return None


def send_message_try(receiver_id: str, message: str, token, account_chat_id):
    print(receiver_id, message, token, account_chat_id)
    headers = {'X-Auth-Token': token}
    url = f'https://amojo.amocrm.ru/v1/chats/{account_chat_id}/' \
          f'{receiver_id}/messages?with_video=true&stand=v15'

    resp = requests.post(url, headers=headers, data=json.dumps({"text": message}))
    return resp.status_code

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


def get_chat_history(receiver_id, token, account_chat_id):
    while True:
        try:
            chat_history = get_chat_history_try(receiver_id, token, account_chat_id)
        except Exception as e:
            token, _ = auth.get_token()
            continue
        break
    return token, chat_history


def send_message(receiver_id, message, account_chat_id, token):
    while True:
        try:
            token, session = auth.get_token()
            status_code = send_message_try(receiver_id, message, account_chat_id, token)
            print(status_code)
        except Exception as e:
            print(e, 'error')
            continue
        if status_code != 200:
            continue
        break
    return token, message