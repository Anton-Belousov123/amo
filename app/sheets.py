import gspread
from oauth2client.service_account import ServiceAccountCredentials


def read_message_preview():
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

    creds = ServiceAccountCredentials.from_json_keyfile_name('misc/chat-384709-f24e97dc0a0b.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('ЧАТ').sheet1
    rules = sheet.cell(1, 1).value
    length = sheet.cell(2, 1).value
    messages = [
        sheet.cell(3, 1).value,
        sheet.cell(4, 1).value,
        sheet.cell(5, 1).value,
        sheet.cell(6, 1).value,
        sheet.cell(7, 1).value,
        sheet.cell(8, 1).value,
                ]
    return rules, length, messages
