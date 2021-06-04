# -*- coding: utf-8 -*-

from config import TOKEN
import telebot
from telebot import types
db = {'Понедельник' : 'пусто', 'Вторник' : 'пусто', 'Среда' : 'пусто', 'Четверг' : 'пусто',
      'Пятница' : 'пусто', 'Суббота' : 'пусто'}

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('index.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('Загрузить')
    item2 = types.KeyboardButton('Получить')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Привет, {0.first_name}! \nЯ помогу тебе всем, чем смогу :)'.format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)
@bot.message_handler(content_types='text')
def choise(message):
    if message.chat.type == 'private':
        if message.text == 'Получить':
            for i in db:
                bot.send_message(message.chat.id, i + ': ' + db[i])
        elif message.text == 'Загрузить':
            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton('Понедельник', callback_data='mo')
            item2 = types.InlineKeyboardButton('Вторник', callback_data='tu')
            item3 = types.InlineKeyboardButton('Среда', callback_data='we')
            item4 = types.InlineKeyboardButton('Четверг', callback_data='th')
            item5 = types.InlineKeyboardButton('Пятница', callback_data='fry')
            item6 = types.InlineKeyboardButton('Суббота', callback_data='sa')
            markup.add(item1, item2, item3, item4, item5, item6)
            bot.send_message(message.chat.id, 'Выберите день недели:', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Я не понимаю!')
def mo(message):
    db['Понедельник'] = message.text
    for i in db:
        bot.send_message(message.chat.id, i + ': ' + db[i])
def tu(message):
    db['Вторник'] = message.text
    for i in db:
        bot.send_message(message.chat.id, i + ': ' + db[i])
def we(message):
    db['Среда'] = message.text
    for i in db:
        bot.send_message(message.chat.id, i + ': ' + db[i])
def th(message):
    db['Четверг'] = message.text
    for i in db:
        bot.send_message(message.chat.id, i + ': ' + db[i])
def fr(message):
    db['Пятница'] = message.text
    for i in db:
        bot.send_message(message.chat.id, i + ': ' + db[i])
def sa(message):
    db['Суббота'] = message.text
    for i in db:
        bot.send_message(message.chat.id, i + ': ' + db[i])

@bot.callback_query_handler(func = lambda call: True)
def callback(call):
    try:
        if call.message:
            if call.data == 'mo':
                msg = bot.send_message(call.message.chat.id, 'Напишите домашнее задание:')
                bot.register_next_step_handler(msg, mo)
            if call.data == 'tu':
                msg = bot.send_message(call.message.chat.id, 'Напишите домашнее задание:')
                bot.register_next_step_handler(msg, tu)
            if call.data == 'we':
                msg = bot.send_message(call.message.chat.id, 'Напишите домашнее задание:')
                bot.register_next_step_handler(msg, we)
            if call.data == 'th':
                msg = bot.send_message(call.message.chat.id, 'Напишите домашнее задание:')
                bot.register_next_step_handler(msg, th)
            if call.data == 'fr':
                msg = bot.send_message(call.message.chat.id, 'Напишите домашнее задание:')
                bot.register_next_step_handler(msg, fr)
            if call.data == 'sa':
                msg = bot.send_message(call.message.chat.id, 'Напишите домашнее задание:')
                bot.register_next_step_handler(msg, sa)
    except Exception as e:
        print(repr(e))

bot.polling()
