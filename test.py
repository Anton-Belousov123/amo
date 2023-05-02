import requests

url = 'https://amojo.amocrm.ru/messages/7eb31c63-e74d-41cd-86f7-34c6265386f9/merge?stand=v15&offset=0&limit=100&chat_id%5B%5D=9389b299-c47b-4607-aad1-3a7baa307bbd&get_tags=true&lang=ru'
print(requests.get(url).text)