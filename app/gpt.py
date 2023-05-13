import os

import openai

from app import sheets
import dotenv

dotenv.load_dotenv('misc/.env')

def prepare_request(amo_messages):
    messages = []
    google_message = sheets.read_message_preview() + ". В твоем сообщении должен быть только ОДИН вопрос." \
                                                     " Ответ должен быть строго в соответствии с лимитом " \
                                                     "знаков который я указал. Ты не должен отправлять никакие свои варианты клиенту." \
                                                     "Действуй строго в последовательности что я указал. Если ты не получил корректный ответ на вопрос, то задай его снова." \
                                                     "Если ты уже задал все вопросы, то ответь спасибо, ожидайте ответа." \
                                                     "Не говори никакую лишнюю информацию не входящую в сценарий!"
    text_length = len(google_message)
    for amo_message in amo_messages:
        if text_length + len(amo_message['text']) > 4000:
            break
        text_length += len(amo_message['text'])
        if amo_message['author']['id'] == '6bbb0237-32bc-4b1f-bcd5-411574e8912c':
            messages.append({"role": "assistant", "content": amo_message['text']})
        else:
            messages.append({"role": "user", "content": amo_message['text']})
    messages.append({'role': 'system', 'content': google_message})
    messages.reverse()
    response = []
    for i in messages:
        if i['content'] == '/restart':
            break
        response.append(i)
    if len(response) == 1:
        response.append({"role": "user", "content": "Привет"})
    return i


def get_answer(messages: list):
    try:
        openai.api_key = os.getenv('CHAT_GPT_KEY')
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response['choices'][0]['message']['content']
    except:
        return get_answer(messages)
