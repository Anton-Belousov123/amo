import os
import time
from flask import Flask, request
import dotenv
from app import gpt, auth, deepl
from app.funcs_amo import get_pipeline, get_chat_history


dotenv.load_dotenv('misc/.env')
token = ''
app = Flask(__name__)
account_chat_id = os.getenv('ACCOUNT_CHAT_ID')


@app.route('/', methods=["POST"])
def hello():
    global token
    d = request.form.to_dict()
    try:
        image = d['message[add][0][author][avatar_url]']
    except:
        image = ''
    name = d['message[add][0][author][name]']
    text = d['message[add][0][text]']
    pipeline = get_pipeline(image, name, text)
    print(pipeline, 'pipeline')
    if pipeline is None or int(d['message[add][0][created_at]']) + 10 < int(time.time()) or d['message[add][0][text]'] == 'Зарегистрироваться в WebApp':
        return 'ok'
    receiver_id = d['message[add][0][chat_id]']
    token, chat_history = get_chat_history(receiver_id, token, account_chat_id)
    lang, text = deepl.translate_it(str(chat_history), 'EN')
    print(text)
    return












    translation = translate_it(text)
    token, session = auth.get_token()
    send_notes(pipeline, session, translation)
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

    if not fl:
        translation = translate_it(message)
        token, session = auth.get_token()
        send_notes(pipeline, session, translation)

    return 'ok'


app.run(host='0.0.0.0', debug=True, port=8000)
