import telebot
from telebot import types #Подключили дополнения
import socket
import datetime
import sqlite3


now = datetime.datetime.now()

bot = telebot.TeleBot('1452247200:AAES4nlaN4zg6-J6ljkDssrcfJYpBVdw3sU')
sock = socket.socket()

#### keys 
register = telebot.types.ReplyKeyboardMarkup(True, True)
register.row('Регистрация') 

admin = telebot.types.ReplyKeyboardMarkup(True, True)
admin.row('Новые заявки')

send_number = telebot.types.ReplyKeyboardMarkup(True, True)
send_number.row('Отправить номер телефона')


#########


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Здравствуйте, {}, для регистрации используйте кнопку 'Регистрация'. ".format(str(message.from_user.first_name) + str(message.from_user.last_name)), reply_markup=register)
    elif message.text == "Регистрация":
        bot.send_message(message.from_user.id, "Для того, что бы зарегистрироваться, следуйте дальнейшим инструкциям бота.")
        bot.send_message(message.from_user.id, "Введите ваше имя: ")
        bot.register_next_step_handler(message, get_name);
    elif message.text == "/admin":
        bot.send_message(message.from_user.id, "Для просмотра новых заявок используйте кнопку.", reply_markup=admin)
    elif message.text == "Новые заявки":
        bot.send_message(message.from_user.id, "Показаны все пользователи которые ожидают заявку на данный момент.\n")
        get_new_user(message)
        #bot.register_next_step_handler(message, go)
    else:
        bot.send_message(message.from_user.id, "Для того что бы зарегистрироваться, используйте - /start")

def get_name(message):
    global name
    global chatid
    global datatime
    datatime = now.strftime("%d-%m-%Y %H:%M")
    chatid = message.from_user.id
    name = message.text
    bot.send_message(message.from_user.id, 'Введите вашу фамилию: ')
    bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    global surname
    surname = message.text

    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)  # Подключаем клавиатуру
    button_phone = types.KeyboardButton(text="Отправить телефон", request_contact=True)  # Указываем название кнопки, которая появится у пользователя
    keyboard.add(button_phone)  # Добавляем эту кнопку

    bot.send_message(message.from_user.id, 'Введите ваш номер телефона: ', reply_markup=keyboard)
    bot.register_next_step_handler(message, get_mobile_phone)

def get_mobile_phone(message):
    global mobilephone
    mobilephone = message.contact
    print(mobilephone)
    insert_sql_new()
    bot.send_message(487348303, "[Запрос регистрации]\nTelegramChatID: {}\nИмя: {}\nФамилия: {}\nМобильный: {}\nДата регистрации: {}".format(chatid, name, surname, mobilephone, datatime))
    bot.send_message(message.from_user.id, "Регистрация завершена, ожидайте одобрения вашей заявки администратором.")





def insert_sql_new():
    try:
        with sqlite3.connect("static/database/main.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Users (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, FirstName TEXT NOT NULL, LastName TEXT NOT NULL, TGUserId INTEGER NOT NULL, MobilePhone NUMERIC NOT NULL, DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Status INTEGER NOT NULL DEFAULT 0)")
            cursor.execute("INSERT INTO Users (FirstName, LastName, TGUserId, MobilePhone, DateCreated, Admin) values ('{}', '{}', '{}', '{}', '{}', '{}')".format(name, surname, chatid, mobilephone, datatime, 0))
            conn.commit()
    except:
        pass


def get_new_user(message):
    gos = telebot.types.ReplyKeyboardMarkup(True, True)

    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users")
        result = cursor.fetchall()
        conn.commit()
        text = ""
        for nu in range(len(result)):
            text = text + str(result[nu]) + "\n"
        for num in result:
            gos.row(str(num[1]) + " " + str(num[2]))
        if len(text) > 4096:
            for x in range(0, len(text), 4096):
                bot.send_message(message.from_user.id, text[x:x + 4096])
        else:
            bot.send_message(message.from_user.id, text, reply_markup=gos)


bot.polling(none_stop=True, timeout=500)

