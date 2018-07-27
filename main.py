import os
from fsm import FSM
from utils import get_image
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

states = FSM(default='answer')
bot = TeleBot(os.environ.get('token'))


@bot.message_handler(commands=['start'])
def start(message):
    return send_captcha(message)


@bot.callback_query_handler(func=lambda call: call.data == 'refresh')
def refresh_captcha(call):
    bot.delete_message(call.from_user.id, message_id=call.message.message_id)
    return send_captcha(call.message)


@bot.message_handler(func=lambda m: states.get_state(m.chat.id))
def receive_answer(message):
    user_id = message.chat.id
    answer = states.get_extra_state(user_id, 'answer')
    if message.text == answer:
        states.remove_state(user_id)
        bot.reply_to(message, text='WELCOME! /start')
    else:
        bot.reply_to(message, text='Wrong, try again!')


def send_captcha(message):
    user_id = message.chat.id
    captcha = get_image()
    states.init_state(user_id)
    states.add_extra_state(user_id, 'answer', captcha['answer'])
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Refresh', callback_data='refresh'))
    bot.send_photo(user_id, captcha['image'], reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True, timeout=100000)
