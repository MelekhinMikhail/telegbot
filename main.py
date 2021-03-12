import telebot
import requests
import schedule
import time

from telebot import types
bot = telebot.TeleBot('1679678375:AAEMgPXpYkMrbSFDJdCKKPMkr5zyShLhHz0')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'Привет, {message.from_user.first_name}! Я бот Ворни. Я буду уведомлять тебя если что-нибудь пойдет не так. Напиши /help, чтобы узнать о моих возможностях.')
@bot.message_handler(commands=['help'])
def send_comlist(message):
    bot.reply_to(message, f'/reg - регистрация\n  /start - начать')

name = '';
surname = '';
age = 0;
def job():
    response = requests.get('http://192.168.1.131/temp')
    bot.reply_to(748853442, f'Температура сейчас: {response.text} C')
def job1():
    humid = requests.get('http://192.168.1.131/humid')
    bot.reply_to(748853442, f'Влажность сейчас: {humid.text} %')
@bot.message_handler(commands=['alert'])
def send_welcome(message):
    print(message.chat.id)
    while True:
        response = requests.get('http://192.168.1.131/temp')
        responseh = requests.get('http://192.168.1.131/humid')
        responses = requests.get('http://192.168.1.131/smoke')
        responsem = requests.get('http://192.168.1.131/move')
        if (float(response.text) > 27 or float(response.text) <18):
            bot.reply_to(message, f'Внимание! Обнаружено резкое изменение температуры! Температура сечас: {response.text} C')
        if (int(responseh.text) > 55 or int(responseh.text) < 40):
            bot.reply_to(message, f'Внимание! Обнаружено резкое изменение влажности! Влажность сечас: {responseh.text} %')
        if (int(responses.text) > 75):
            bot.reply_to(message, f'Внимание! Обнаружено резкое повышение метана! Уровень метана сечас: {responses.text} ppm')
        if (int(responsem.text) == 1):
            bot.reply_to(message, f'Внимание! Обнаружено движение!')
        time.sleep(10)


@bot.message_handler(commands=['humid1'])
def send_welcome(message):
    print(message.chat.id)
    while True:
        response = requests.get('http://192.168.1.131/humid')
        if (int(response.text) < 25):
            bot.reply_to(message, f'Влажность сейчас: {response.text} %')
        time.sleep(10)

@bot.message_handler(commands=['humid'])
def send_welcome(message):
    print(message.chat.id)
    response = requests.get('http://192.168.1.131/humid')
    bot.reply_to(message, f'Влажность сейчас: {response.text} %')

@bot.message_handler(commands=['temp'])
def send_welcome(message):
    response = requests.get('http://192.168.1.131/temp')
    bot.reply_to(message, f'Температура сейчас: {response.text} С')


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text.lower() == '/reg':
        bot.send_message(message.from_user.id, "Как тебя зовут?");
        bot.register_next_step_handler(message, get_name); #следующий шаг – функция get_name
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg');

def get_name(message): #получаем фамилию
    global name;
    name = message.text;
    bot.send_message(message.from_user.id, 'Какая у тебя фамилия?');
    bot.register_next_step_handler(message, get_surname);

def get_surname(message):
    global surname;
    surname = message.text;
    bot.send_message(message.from_user.id, 'Сколько тебе лет?');
    bot.register_next_step_handler(message, get_age);

def get_age(message):
    global age;
    while age == 0: #проверяем что возраст изменился
        try:
             age = int(message.text) #проверяем, что возраст введен корректно
        except Exception:
             bot.send_message(message.from_user.id, 'Цифрами, пожалуйста');
    bot.send_message(message.from_user.id, 'Тебе '+str(age)+' лет, тебя зовут '+name+' '+surname+'?')

def get_age(message):
    global age;
    while age == 0: #проверяем что возраст изменился
        try:
             age = int(message.text) #проверяем, что возраст введен корректно
        except Exception:
             bot.send_message(message.from_user.id, 'Цифрами, пожалуйста');
    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
    keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_no);
    question = 'Тебе '+str(age)+' лет, тебя зовут '+name+' '+surname+'?';
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        ... #код сохранения данных, или их обработки
        bot.send_message(call.message.chat.id, 'Запомню : )');
    elif call.data == "no":
        ... #переспрашиваем
        bot.send_message(call.message.chat.id, 'Не обманывай, я записывал :)');
schedule.run_pending()
bot.polling(none_stop=True)
