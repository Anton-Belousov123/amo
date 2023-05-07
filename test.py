import requests


r = requests.post('http://172.22.0.2:80', data={
    'test': '123'
})
print(r.text)