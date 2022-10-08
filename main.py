# -*- coding: utf-8 -*-
from config import TOKEN
import telebot
import os
import uuid
import speech_recognition as sr
from fuzzywuzzy import fuzz
from telebot import types
db = {'Понедельник' : 'пусто', 'Вторник' : 'пусто', 'Среда' : 'пусто', 'Четверг' : 'пусто',
      'Пятница' : 'пусто', 'Суббота' : 'пусто'}

bot = telebot.TeleBot(TOKEN)
language='ru_RU'
r = sr.Recognizer()

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('index.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('Загрузить')
    item2 = types.KeyboardButton('Получить')
    item3 = types.KeyboardButton('Расписание')
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, 'Привет, {0.first_name}!\nСамое время начать учиться :)'.format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['Social_Studies'])
def social(message):
    msg = bot.send_message(message.chat.id, 'Напиши номер параграфа:')
    bot.register_next_step_handler(msg, social_studies)
def social_studies(message):
    paragraf = message.text
    bot.send_message(message.chat.id, 'https://resheba.me/gdz/obshhestvoznanie/11-klass/bogoljubov/paragraph-%s'%(paragraf))



@bot.message_handler(commands=['English_workbook'])
def eng(message):
    bot.send_message(message.chat.id, 'Пока не работает')


@bot.message_handler(commands=['English_textbook'])
def engl(message):
    msg = bot.send_message(message.chat.id, 'Напиши через пробел сначала юнит, затем номер и ноль в конце\nЕсли это Progress Check, тогда в конце замени "0" на его юнит')
    bot.register_next_step_handler(msg, english_textbook)
def english_textbook(message):
    unit, number, p_check = map(str, message.text.split())
    if p_check == '0':
        bot.send_message(message.chat.id, 'https://megaresheba.ru/gdz/anglijskij-yazyk/11-klass/enjoy-english-biboletova-snezhko/%s-unit-%s'%(unit, number))
    else:
        bot.send_message(message.chat.id, 'https://megaresheba.ru/gdz/anglijskij-yazyk/11-klass/enjoy-english-biboletova-snezhko/%s-check-%s'%(unit, number))

@bot.message_handler(content_types='text')
def choise(message):
    if message.chat.type == 'private':
        if message.text == 'Отправь фото':
            photo = open('random_photo.jpg', 'rb')
            bot.send_photo(message.chat.id, photo)
        elif message.text == 'ГДЗ':
            bot.send_message(message.chat.id, 'Доступные предметы:\n/English_textbook (англ. учебник)\n/Social_Studies (Обществознание)\n/English_workbook (анг раб.тет.\n)')
        elif message.text == 'Получить':
            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton('Понедельник', callback_data='mo2')
            item2 = types.InlineKeyboardButton('Вторник', callback_data='tu2')
            item3 = types.InlineKeyboardButton('Среда', callback_data='we2')
            item4 = types.InlineKeyboardButton('Четверг', callback_data='th2')
            item5 = types.InlineKeyboardButton('Пятница', callback_data='fr2')
            item6 = types.InlineKeyboardButton('Суббота', callback_data='sa2')
            markup.add(item1, item2, item3, item4, item5, item6)
            bot.send_message(message.chat.id, 'Выберите день недели:', reply_markup=markup)
        elif message.text == 'Загрузить':
            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton('Понедельник', callback_data='mo')
            item2 = types.InlineKeyboardButton('Вторник', callback_data='tu')
            item3 = types.InlineKeyboardButton('Среда', callback_data='we')
            item4 = types.InlineKeyboardButton('Четверг', callback_data='th')
            item5 = types.InlineKeyboardButton('Пятница', callback_data='fr')
            item6 = types.InlineKeyboardButton('Суббота', callback_data='sa')
            markup.add(item1, item2, item3, item4, item5, item6)
            bot.send_message(message.chat.id, 'Выберите день недели:', reply_markup=markup)
        elif message.text == 'Расписание':
            markup = types.InlineKeyboardMarkup(row_width=3)
            item1 = types.InlineKeyboardButton('Понедельник', callback_data='mo1')
            item2 = types.InlineKeyboardButton('Вторник', callback_data='tu1')
            item3 = types.InlineKeyboardButton('Среда', callback_data='we1')
            item4 = types.InlineKeyboardButton('Четверг', callback_data='th1')
            item5 = types.InlineKeyboardButton('Пятница', callback_data='fr1')
            item6 = types.InlineKeyboardButton('Суббота', callback_data='sa1')
            markup.add(item1, item2, item3, item4, item5, item6)
            bot.send_message(message.chat.id, 'Выберите день недели:', reply_markup=markup)
        else:
            q = open('q.txt')
            list_q = []
            list_a = []
            for i in q:
                list_q.append(i.rstrip())
            a = open('a.txt')
            for i in a:
    	        list_a.append(i.rstrip())
            q.close()
            a.close()

            for i in range(len(list_q)):
                if (fuzz.ratio(message.text, list_q[i])) > 66:
                    bot.send_message(message.chat.id, list_a[i])
                    break

def recognise(filename):
    with sr.AudioFile(filename) as source:
        audio_text = r.listen(source)
        try:
            text = r.recognize_google(audio_text,language=language)
            return text
        except:
            return "Говорите четче!"

def mo(message):
    if message.content_type == 'photo':
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)

        with open('monday.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)
    elif message.content_type == 'voice':
        filename = str(uuid.uuid4())
        file_name_full="./voice/"+filename+".ogg"
        file_name_full_converted="./ready/"+filename+".wav"
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_name_full, 'wb') as new_file:
            new_file.write(downloaded_file)
        os.system("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)
        text=recognise(file_name_full_converted)

        db['Понедельник'] = text
        bot.send_message(message.chat.id, 'Понедельник: ' + db['Понедельник'])
        os.remove(file_name_full)
        os.remove(file_name_full_converted)

    else:
        db['Понедельник'] = message.text
        bot.send_message(message.chat.id, 'Понедельник: ' + db['Понедельник'])
def tu(message):
    if message.content_type == 'photo':
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)

        with open('tuesday.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)
    elif message.content_type == 'voice':
        filename = str(uuid.uuid4())
        file_name_full="./voice/"+filename+".ogg"
        file_name_full_converted="./ready/"+filename+".wav"
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_name_full, 'wb') as new_file:
            new_file.write(downloaded_file)
        os.system("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)
        text=recognise(file_name_full_converted)

        db['Вторник'] = text
        bot.send_message(message.chat.id, 'Вторник: ' + db['Вторник'])
        os.remove(file_name_full)
        os.remove(file_name_full_converted)

    else:
        db['Вторник'] = message.text
        bot.send_message(message.chat.id, 'Вторник: ' + db['Вторник'])
def we(message):
    if message.content_type == 'photo':
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)

        with open('wesday.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)
    elif message.content_type == 'voice':
        filename = str(uuid.uuid4())
        file_name_full="./voice/"+filename+".ogg"
        file_name_full_converted="./ready/"+filename+".wav"
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_name_full, 'wb') as new_file:
            new_file.write(downloaded_file)
        os.system("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)
        text=recognise(file_name_full_converted)

        db['Среда'] = text
        bot.send_message(message.chat.id, 'Среда: ' + db['Среда'])
        os.remove(file_name_full)
        os.remove(file_name_full_converted)

    else:
        db['Среда'] = message.text
        bot.send_message(message.chat.id, 'Среда: ' + db['Среда'])
def th(message):
    if message.content_type == 'photo':
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)

        with open('thuesday.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)
    elif message.content_type == 'voice':
        filename = str(uuid.uuid4())
        file_name_full="./voice/"+filename+".ogg"
        file_name_full_converted="./ready/"+filename+".wav"
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_name_full, 'wb') as new_file:
            new_file.write(downloaded_file)
        os.system("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)
        text=recognise(file_name_full_converted)

        db['Четверг'] = text
        bot.send_message(message.chat.id, 'Четверг: ' + db['Четверг'])
        os.remove(file_name_full)
        os.remove(file_name_full_converted)

    else:
        db['Четверг'] = message.text
        bot.send_message(message.chat.id, 'Четверг: ' + db['Четверг'])
def fr(message):
    if message.content_type == 'photo':
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)

        with open('friday.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)
    elif message.content_type == 'voice':
        filename = str(uuid.uuid4())
        file_name_full="./voice/"+filename+".ogg"
        file_name_full_converted="./ready/"+filename+".wav"
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_name_full, 'wb') as new_file:
            new_file.write(downloaded_file)
        os.system("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)
        text=recognise(file_name_full_converted)

        db['Пятница'] = text
        bot.send_message(message.chat.id, 'Пятница: ' + db['Пятница'])
        os.remove(file_name_full)
        os.remove(file_name_full_converted)

    else:
        db['Пятница'] = message.text
        bot.send_message(message.chat.id, 'Пятница: ' + db['Пятница'])
def sa(message):
    if message.content_type == 'photo':
        fileID = message.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)

        with open('saturday.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)

    elif message.content_type == 'voice':
        filename = str(uuid.uuid4())
        file_name_full="./voice/"+filename+".ogg"
        file_name_full_converted="./ready/"+filename+".wav"
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(file_name_full, 'wb') as new_file:
            new_file.write(downloaded_file)
        os.system("ffmpeg -i "+file_name_full+"  "+file_name_full_converted)
        text=recognise(file_name_full_converted)

        db['Суббота'] = text
        bot.send_message(message.chat.id, 'Суббота: ' + db['Суббота'])
        os.remove(file_name_full)
        os.remove(file_name_full_converted)
    else:
        db['Суббота'] = message.text
        bot.send_message(message.chat.id, 'Суббота: ' + db['Суббота'])


r_mo = """
Понедельник
1. Алгебра
2. Химия
3. Русский
4. Физ-ра
5. География
6. Информатика
7. Инд. проект(дист.)"""
r_tu = """
Вторник
1. Геометрия
2.Биология
3. Обществознание
4. Русский
5. Литература
6. Физика
7. ОБЖ"""
r_we = """
Среда
1. Алгебра
2. Алгебра
3. Литература
4. Литература
5. Ин. яз.
6. Физ-ра
7. Обществознание"""
r_th = """
Четверг
1.Алгебра
2. История
3. История
4. Биология
5. Физика
6. Ин. яз."""
r_fr = """
Пятница
1. Алгебра
2. Геометрия
3. Общество
4. Литература
5. Физ-ра
6. Химия"""
r_sa = """
Суббота
1. Ин. яз.
2. МХК
3. История Ставрополья
4. Информатика"""


@bot.message_handler(content_types=['photo'])
def photo(message):
    print('message.photo=', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID=', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path=', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)

    with open('random_photo.jpg', 'wb') as new_file:
        new_file.write(downloaded_file)

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
            if call.data == 'mo1':
                bot.send_message(call.message.chat.id, r_mo)
            if call.data == 'tu1':
                bot.send_message(call.message.chat.id, r_tu)
            if call.data == 'we1':
                bot.send_message(call.message.chat.id, r_we)
            if call.data == 'th1':
                bot.send_message(call.message.chat.id, r_th)
            if call.data == 'fr1':
                bot.send_message(call.message.chat.id, r_fr)
            if call.data == 'sa1':
                bot.send_message(call.message.chat.id, r_sa)
            if call.data == 'mo2':
                bot.send_message(call.message.chat.id, 'Понедельник: ' + db['Понедельник'])
                photo = open('monday.jpg', 'rb')
                bot.send_photo(call.message.chat.id, photo)
            if call.data == 'tu2':
                bot.send_message(call.message.chat.id, 'Вторник: ' + db['Вторник'])
                photo = open('tuesday.jpg', 'rb')
                bot.send_photo(call.message.chat.id, photo)
            if call.data == 'we2':
                bot.send_message(call.message.chat.id, 'Среда: ' + db['Среда'])
                photo = open('wesday.jpg', 'rb')
                bot.send_photo(call.message.chat.id, photo)
            if call.data == 'th2':
                bot.send_message(call.message.chat.id, 'Четверг: ' + db['Четверг'])
                photo = open('thuesday.jpg', 'rb')
                bot.send_photo(call.message.chat.id, photo)
            if call.data == 'fr2':
                bot.send_message(call.message.chat.id, 'Пятница: ' + db['Пятница'])
                photo = open('friday.jpg', 'rb')
                bot.send_photo(call.message.chat.id, photo)
            if call.data == 'sa2':
                bot.send_message(call.message.chat.id, 'Суббота: ' + db['Суббота'])
                photo = open('saturday.jpg', 'rb')
                bot.send_photo(call.message.chat.id, photo)
    except Exception as e:
        print(repr(e))

bot.infinity_polling(timeout=10, long_polling_timeout=5)
