import logging
import os
from random import randint

import requests
from dotenv import load_dotenv
from telegram import Bot
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

load_dotenv()
TG_TOKEN = os.getenv('TOKEN')
TG_CHAT_ID = os.getenv('MY_TG_ID')

URL = 'https://api.thecatapi.com/v1/images/search'

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        # logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
    random_cat = response.json()[0].get('url')
    return random_cat


def show_new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())


def wake_me_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup(keyboard=[
        ['/new_cat'],
        ['Который час?', 'Определи мой ip'],
        ['/random_digit', '/start'],
        ],
        resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Спасибо, что включили меня, {name}. '
             f'Посмотрите, какого котика я Вам нашёл',
        reply_markup=button
    )
    context.bot.send_photo(chat.id, get_new_image())


def say_hi(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Привет, я KittyBot!')


def show_random_int(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=randint(0, 100))


def main():
    bot = Bot(token=TG_TOKEN)
    bot.send_message(TG_CHAT_ID, 'Привет, я проснулся!')
    updater = Updater(token=TG_TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', wake_me_up))
    updater.dispatcher.add_handler(CommandHandler('new_cat', show_new_cat))
    updater.dispatcher.add_handler(
        CommandHandler('random_digit', show_random_int))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
