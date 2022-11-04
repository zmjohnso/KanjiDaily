import random

import requests
import telebot
from decouple import config

API_KEY = config('API_KEY_TG')
bot = telebot.TeleBot(API_KEY, parse_mode=None)

kanjiapi_url = 'kanjiapi.dev'

@bot.message_handler(commands=['kanji'])
def kanji(message):
    response = requests.get(f'https://{kanjiapi_url}/v1/kanji/joyo')
    if response.status_code == 200:
        length = len(response.json())
        random_kanji = response.json()[random.randint(0, length - 1)]
        meaning = requests.get(f'https://{kanjiapi_url}/v1/kanji/{random_kanji}')
        if meaning.status_code == 200:
            random_kanji_meaning = meaning.json()['meanings']
            full_message = f'{random_kanji}: '
            for val in random_kanji_meaning:
                full_message += val + ', '
            # remove trailing ', '
            full_message = full_message[:-2]
            bot.send_message(message.chat.id, full_message)

# bot.infinity_polling()


# @bot.message_handler(commands=['meaning'])
# def kanji(message):
#     response = requests.get(f'https://{kanjiapi_url}/v1/kanji/joyo')
#     if response.status_code == 200:
#         length = len(response.json())
#         random_kanji = response.json()[random.randint(0, length - 1)]
#         bot.send_message(message.chat.id, random_kanji)
