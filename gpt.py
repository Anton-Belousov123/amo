import openai

import sheets


def prepare_request(amo_messages):
    messages = []
    google_message = sheets.read_message_preview()
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
    return messages

def get_answer(messages: list):
    try:
        openai.api_key = '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'
        response = openai.ChatCompletion.create(
          model="gpt-3.5-turbo",
          messages=messages
        )
        return response['choices'][0]['message']['content']
    except:
        return get_answer(messages)
