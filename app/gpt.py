import os

import openai

from app import sheets
import dotenv

dotenv.load_dotenv('misc/.env')


def what_is_the_question(question, m):
    task = [{'role': 'system', 'content': 'Есть текст. Твоя задача написать цифру, к которой относится данный вопрос.'
                                          f' Возможные варианты: 0 - {m[0]};'
                                          f'1 - {m[1]};'
                                          f'2 - {m[2]};'
                                          f'3 - {m[3]};'
                                          f'4 - {m[4]};'
                                          f'5 - {m[5]};'
                                          f'6 - {m[6]};'
             }]
    task.append({'role': 'user', 'content': question})
    answer = get_answer(task, 1)
    while answer != '0' and answer != '1' and answer != '2' and answer != '3' and answer != '4' and answer != '5' and answer != '6':
        answer = get_answer(task, 1)
    print('message id: ', answer)
    return int(answer)


def is_answer_correct(question, answer):
    task = [{'role': 'system', 'content': 'У тебя есть вопрос и ответ. Твоя задача сказать, является этот '
                                          'ответ корректным на данный вопрос (то есть что ответ совпадает по '
                                          'смыслу с вопросом). Если ответ корректен - выведи цифру 1, если нет - 0'}]
    task.append({'role': 'assistant', 'content': "Вопрос: " + question})
    task.append({'role': 'user', 'content': "Ответ: " + answer})
    answer = get_answer(task, 1)
    while answer != '1' or answer != '0':
        answer = get_answer(task, 1)
    print('is correct: ', answer)
    return int(answer)


def prepare_request(amo_messages):
    messages = []
    print(amo_messages)
    rules, length, messages = sheets.read_message_preview()
    index = what_is_the_question(amo_messages[1], messages)
    status = is_answer_correct(amo_messages[1], amo_messages[0])
    text_length = len(rules)
    if status == 0 or index + 1 >= len(messages):
        messages.append({'role': 'system', 'content': messages[index]})
    else:
        messages.append({'role': 'system', 'content': messages[index + 1]})
    for amo_message in amo_messages:
        if text_length + len(amo_message['text']) > 4000:
            break
        text_length += len(amo_message['text'])
        if amo_message['author']['id'] == '6bbb0237-32bc-4b1f-bcd5-411574e8912c':
            messages.append({"role": "assistant", "content": amo_message['text']})
        else:
            messages.append({"role": "user", "content": amo_message['text']})
    messages.append({'role': 'system', 'content': rules})

    response = []
    for i in messages:
        if i['content'] == '/restart':
            break
        response.append(i)
    if len(response) == 0:
        response.append({"role": "user", "content": "Привет. Я новый клиент. Разговаривай со мной на моем языке"})
        response.append({'role': 'system', 'content': rules})
        response.append({'role': 'system', 'content': messages[0]})
    response.reverse()
    print(response)
    return response


def get_answer(messages: list, limit):
    print(messages)
    try:
        # if True:
        openai.api_key = os.getenv('CHAT_GPT_KEY')
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=int(limit)
        )
        print(response, 'response')

        return response['choices'][0]['message']['content']

    except Exception as e:
        print('Ошибка', e)
        return get_answer(messages)
