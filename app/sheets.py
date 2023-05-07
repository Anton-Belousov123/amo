import gspread
from oauth2client.service_account import ServiceAccountCredentials


def read_message_preview() -> str:
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name('misc/chat-384709-f24e97dc0a0b.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('ЧАТ').sheet1
    value = sheet.cell(1, 1).value
    return value
