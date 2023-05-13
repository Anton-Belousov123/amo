import requests
import hashlib
import hmac
import datetime


# Constants
secret = 'c506ff3d57fca1998e50ea8076ef7afc27934f65'
conversation_id = '9389b299-c47b-4607-aad1-3a7baa307bbd'
scope_id = '0de9c1dd-b5d8-4b38-bb7f-ef238bb3ca86_7eb31c63-e74d-41cd-86f7-34c6265386f9'

# Usable variables
date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
content_type = 'application/json'
path = f'/v2/origin/custom/{scope_id}/chats/{conversation_id}/history'
url = f'https://amojo.amocrm.ru' + path


# Main login
check_sum = hashlib.md5(b'').hexdigest()
message = '\n'.join(["GET", check_sum, content_type, date, path]).encode('utf-8')
signature = hmac.new(secret.encode('utf-8'), message, hashlib.sha1).hexdigest()


# Request
headers = {
    'Date': date,
    'Content-Type': content_type,
    'Content-MD5': check_sum.lower(),
    'X-Signature': signature.lower(),
}
response = requests.get(url=url, headers=headers)

print(f"Status: {response.status_code}")
print(response.text)