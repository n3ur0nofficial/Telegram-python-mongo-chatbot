import requests
import datetime
#from responses import *
from mongoResponse import *
import spacyOps
from spacyOps import *
import pandas as ppd
from bson import ObjectId


class BotHandler:
    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    # url = "https://api.telegram.org/bot&lt;token>/"

    def get_updates(self, offset=0, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_first_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[0]
        else:
            last_update = None

        return last_update


token = '890253007:AAFTr10DH-1bkPwZy4ZjdBr_cbH7dF57kKw'

RMDSI_bot = BotHandler(token)  ## YOU CAN GIVE A DIFFERENT NAME for BotHandler
greetings = ('hello', 'hi', 'greetings', 'whatsup')
abuses = ('idiot', 'mad', 'donkey', 'nerdd')
def main():
    new_offset = 0
    print('This is a cool bot...')

    while True:

        all_updates = RMDSI_bot.get_updates(new_offset)
        if len(all_updates) > 0:
            for current_update in all_updates:
                print(current_update)
                first_update_id = current_update['update_id']
                if 'text' not in current_update['message']:
                    first_chat_text = 'New member'
                else:
                    first_chat_text = current_update['message']['text']
                first_chat_id = current_update['message']['chat']['id']
                if 'first_name' in current_update['message']:
                    first_chat_name = current_update['message']['chat']['first_name']
                elif 'new_chat_member' in current_update['message']:
                    first_chat_name = current_update['message']['new_chat_member']['username']
                elif 'from' in current_update['message']:
                    first_chat_name = current_update['message']['from']['first_name']
                else:
                    first_chat_name = "unknown"

                if first_chat_text.casefold() in greetings:
                    RMDSI_bot.send_message(first_chat_id,
                                               'Greetings from RMDSI Bot, ' + first_chat_name + '!!\n')
                    RMDSI_bot.send_message(first_chat_id, 'How can I help you? ' + first_chat_name)
                    new_offset = first_update_id + 1
                elif first_chat_text.casefold() in abuses:
                    RMDSI_bot.send_message(first_chat_id, 'Pls dont abuse, I am a brilliant bot ' + first_chat_name + '!!\n')
                    new_offset = first_update_id + 1
                elif first_chat_text.casefold() not in greetings and abuses:
                    ne = spacyOps.Tokenizing.tokenizing(first_chat_text)
                    bot_response = mongoResponse.mongoResponse(ne, "testdb", "testcol")
                    for index, row in bot_response.astype(str).iterrows():
                        RMDSI_bot.send_message(first_chat_id, row['c1'] + '-->' + row['c2'])
                    new_offset = first_update_id + 1


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()