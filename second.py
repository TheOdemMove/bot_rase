import telebot
from telebot import types
import datetime
import sqlite3
import re
from PIL import Image, ImageDraw, ImageFont



bot = telebot.TeleBot('1173276637:AAGcELhOEt6KULo7GWYNohCXWw2YtvwqXUE')
now = datetime.datetime.now()

@bot.message_handler(commands=['start'])
def phone(message):
    if message.chat.type == 'private':
        check = check_reg(message.from_user.id)
        if check == 1:
            register = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button_phone = types.KeyboardButton(text="Регистрация")
            register.add(button_phone)
            bot.send_message(message.from_user.id, "Здравствуйте, {}, для регистрации используйте кнопку 'Регистрация'. ".format(str(message.from_user.first_name)), reply_markup=register)
        elif check == 2:
            bot.send_message(message.from_user.id, "Вы уже подали заявку на регистрацию, пожалуйста, ожидайте ее одоборения.")
        elif check == 3:
            bot.send_message(message.from_user.id, "Используйте меню для выбора функций.", reply_markup=default_menu_user())
        elif check == 4:
            bot.send_message(message.from_user.id, "[You Admin] Используйте меню для выбора функций. ", reply_markup=default_menu_admin())
    else:
        bot.send_message(message.chat.id, "Иди нахуй, в лс пиши.")



def check_reg(id):
    try:
        with sqlite3.connect("static/database/main.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Users (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, FirstName TEXT NOT NULL, LastName TEXT NOT NULL, TGUserId INTEGER NOT NULL, MobilePhone NUMERIC NOT NULL, DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Status INTEGER NOT NULL DEFAULT 2, Alerts INTEGER NOT NULL DEFAULT 0)")
            cursor.execute("SELECT * FROM Users WHERE TGUserId={}".format(id))
            result = cursor.fetchone()
            conn.commit()
        if result[3] == id:
            if result[6] == 2:
                back = 2
            elif result[6] == 3:
                back = 3
            elif result[6] == 4:
                back = 4
            return back
        else:
            back = 1
        return back
    except:
        back = 1
        return back







@bot.message_handler(content_types=['text'])
def work(message):
    if message.chat.type == 'private':
        check = check_reg(message.from_user.id)
        if check == 1:
            if message.text == 'Регистрация':
                ###
                register = types.ReplyKeyboardRemove()
                ###
                bot.send_message(message.from_user.id, "Для того, что бы зарегистрироваться, следуйте дальнейшим инструкциям бота.", reply_markup=register)
                bot.send_message(message.from_user.id, "Введите ваше имя: ")
                bot.register_next_step_handler(message, get_name)
            else:
                bot.send_message(message.from_user.id, 'Простите, я не понимаю вас, используйте команду - /start', reply_markup=default_start_button())
        elif check == 2:
            bot.send_message(message.from_user.id, "Вы уже подали заявку на регистрацию, пожалуйста, ожидайте ее одоборения.")
        elif check == 3:
            if message.text == 'Мои автомобили':
                get_car_user(message)
            elif message.text == 'Регистрация на мероприятие':
                show_mp_menu(message)
            elif message.text == 'Мой ТОП-10':
                top_race(message)
            elif message.text == 'Общий ТОП-10':
                all_top_race(message)
            elif message.text == 'Настройки':
                usr_setting(message)

            else:
                bot.send_message(message.from_user.id, 'Простите, я не понимаю вас, используйте меню.', reply_markup=default_menu_user())
        elif check == 4:
            if message.text == 'Панель администратора':
                bot.send_message(message.from_user.id, "Используйте меню, для выбора действий.", reply_markup=default_menu_admin_action())
                bot.register_next_step_handler(message, admin_panel)
            elif message.text == 'Мои автомобили':
                get_car_user(message)
            elif message.text == 'Регистрация на мероприятие':
                show_mp_menu(message)
            elif message.text == 'Мой ТОП-10':
                top_race(message)
            elif message.text == 'Общий ТОП-10':
                all_top_race(message)
            elif message.text == 'Настройки':
                usr_setting(message)
            else:
                bot.send_message(message.from_user.id, 'Простите, я не понимаю вас, используйте меню.', reply_markup=default_menu_admin())


def usr_setting(message):
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Users (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, FirstName TEXT NOT NULL, LastName TEXT NOT NULL, TGUserId INTEGER NOT NULL, MobilePhone NUMERIC NOT NULL, DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Status INTEGER NOT NULL DEFAULT 2, Alerts INTEGER NOT NULL DEFAULT 0)")
        cursor.execute("SELECT * FROM Users WHERE  TGUserId={}".format(message.from_user.id))
        result = cursor.fetchone()
    mycar = telebot.types.ReplyKeyboardMarkup(True, True)
    mycar.row('Личная информация')
    mycar.row('Изменить данные о себе')
    if result[7] == 0:
        mycar.row('Выключить оповещения')
    elif result[7] == 1:
        mycar.row('Включить оповещения')
    mycar.row('<< Назад')
    bot.send_message(message.from_user.id, 'Выберите действие, которое хотите сделать.', reply_markup=mycar)
    bot.register_next_step_handler(message, next_usr_setting)

def next_usr_setting(message):
    check = check_reg(message.from_user.id)
    if message.text == 'Изменить данные о себе':
        #####
        change_info = telebot.types.ReplyKeyboardMarkup(True, True)
        change_info.row('Имя')
        change_info.row('Фамилия')
        change_info.row('Номер телефона')
        change_info.row('<< Назад')
        #####
        bot.send_message(message.from_user.id, 'Выберите какие данные хотите изменить.', reply_markup=change_info)
        bot.register_next_step_handler(message, next_change_info)
        #usr_setting(message)
    elif message.text == 'Выключить оповещения':
        ##
        with sqlite3.connect("static/database/main.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Users (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, FirstName TEXT NOT NULL, LastName TEXT NOT NULL, TGUserId INTEGER NOT NULL, MobilePhone NUMERIC NOT NULL, DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Status INTEGER NOT NULL DEFAULT 2, Alerts INTEGER NOT NULL DEFAULT 0)")
            cursor.execute("UPDATE Users SET Alerts=1 WHERE TGUserId={}".format(message.from_user.id))
            conn.commit()
        bot.send_message(message.from_user.id, 'Вы успешно *отключили* оповещения.\nЭто значит, что вы не будете получать смс о доступных новых мероприятиях.', parse_mode="Markdown")
        usr_setting(message)
        ##
    elif message.text == 'Личная информация':
        with sqlite3.connect("static/database/main.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Users (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, FirstName TEXT NOT NULL, LastName TEXT NOT NULL, TGUserId INTEGER NOT NULL, MobilePhone NUMERIC NOT NULL, DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Status INTEGER NOT NULL DEFAULT 2, Alerts INTEGER NOT NULL DEFAULT 0)")
            cursor.execute("SELECT * FROM Users WHERE TGUserId={}".format(message.from_user.id))
            conn.commit()
        result_usr = cursor.fetchone()
        if result_usr[7] == 1:
            alerts = 'Выключены'
        elif result_usr[7] == 0:
            alerts = 'Включены'
        if result_usr[6] == 3:
            status_usr = 'Пользователь'
        elif result_usr[6] == 4:
            status_usr = 'Администратор'
        bot.send_message(message.from_user.id, '-----(Личная информация)-----\nИмя: *{}*\nФамилия: *{}*\nМобильный: *{}*\nДата регистрации: *{}*\nСтатус: *{}*\nОповещения: *{}*'.format(result_usr[1], result_usr[2], result_usr[4], result_usr[5], status_usr, alerts), parse_mode="Markdown")
        usr_setting(message)
    elif message.text == 'Включить оповещения':
        with sqlite3.connect("static/database/main.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Users (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, FirstName TEXT NOT NULL, LastName TEXT NOT NULL, TGUserId INTEGER NOT NULL, MobilePhone NUMERIC NOT NULL, DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Status INTEGER NOT NULL DEFAULT 2, Alerts INTEGER NOT NULL DEFAULT 0)")
            cursor.execute("UPDATE Users SET Alerts=0 WHERE TGUserId={}".format(message.from_user.id))
            conn.commit()
        bot.send_message(message.from_user.id, 'Вы успешно *включили* оповещения.\nЭто значит, что вы будете получать смс о доступных новых мероприятиях.', parse_mode="Markdown")
        usr_setting(message)
    elif message.text == '<< Назад':
        if check == 3:
            bot.send_message(message.from_user.id, 'Вы вернулись в главное меню.', reply_markup=default_menu_user())
        elif check == 4:
            bot.send_message(message.from_user.id, 'Вы вернулись в главное меню.', reply_markup=default_menu_admin())
    else:
        bot.send_message(message.from_user.id, 'Вы говорите какую-то неправду, попробуйте снова.')
        usr_setting(message)



def next_change_info(message):
    but = telebot.types.ReplyKeyboardRemove()
    if message.text == 'Имя':
        bot.send_message(message.from_user.id, 'Укажите пожалуйста новое имя: ', reply_markup=but)
        bot.register_next_step_handler(message, change_name_usr)
        ####
    elif message.text == 'Фамилия':
        bot.send_message(message.from_user.id, 'Укажите пожалуйста новое фамилию: ', reply_markup=but)
        bot.register_next_step_handler(message, change_surname_usr)
    elif message.text == 'Номер телефона':
        bot.send_message(message.from_user.id, 'Укажите пожалуйста новый номер телефона: ', reply_markup=but)
        bot.register_next_step_handler(message, change_mobile_usr)
    elif message.text == '<< Назад':
        usr_setting(message)

def change_name_usr(message):
    newname = message.text
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Users (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, FirstName TEXT NOT NULL, LastName TEXT NOT NULL, TGUserId INTEGER NOT NULL, MobilePhone NUMERIC NOT NULL, DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Status INTEGER NOT NULL DEFAULT 2, Alerts INTEGER NOT NULL DEFAULT 0)")
        cursor.execute("UPDATE Users SET FirstName='{}' WHERE TGUserId={}".format(newname, message.from_user.id))
        conn.commit()
    bot.send_message(message.from_user.id, 'Вы успешно изменили имя на: *{}* '.format(newname), parse_mode="Markdown")
    usr_setting(message)

def change_surname_usr(message):
    newsurname = message.text
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Users (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, FirstName TEXT NOT NULL, LastName TEXT NOT NULL, TGUserId INTEGER NOT NULL, MobilePhone NUMERIC NOT NULL, DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Status INTEGER NOT NULL DEFAULT 2, Alerts INTEGER NOT NULL DEFAULT 0)")
        cursor.execute("UPDATE Users SET LastName='{}' WHERE TGUserId={}".format(newsurname, message.from_user.id))
        conn.commit()
    bot.send_message(message.from_user.id, 'Вы успешно изменили фамилию на: *{}* '.format(newsurname), parse_mode="Markdown")
    usr_setting(message)

def change_mobile_usr(message):
    newmobile = message.text
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Users (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, FirstName TEXT NOT NULL, LastName TEXT NOT NULL, TGUserId INTEGER NOT NULL, MobilePhone NUMERIC NOT NULL, DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Status INTEGER NOT NULL DEFAULT 2, Alerts INTEGER NOT NULL DEFAULT 0)")
        cursor.execute("UPDATE Users SET MobilePhone='{}' WHERE TGUserId={}".format(newmobile, message.from_user.id))
        conn.commit()
    bot.send_message(message.from_user.id, 'Вы успешно изменили мобильный номер на: *{}* '.format(newmobile), parse_mode="Markdown")
    usr_setting(message)

def top_race(message):
    check = check_reg(message.chat.id)
    delb = telebot.types.ReplyKeyboardRemove()
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS MP_Result (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpId INTEGER NOT NULL, MpUserId INTEGER NOT NULL, Result FLOAT, UserCar TEXT NOT NULL, UStatus INTEGER NOT NULL, Privod TEXT, Rezina TEXT)")
        cursor.execute("SELECT * FROM MP_Result WHERE (MpUserId={}) AND (Ustatus=1) ORDER BY Result LIMIT 10".format(message.chat.id))
        conn.commit()
    result = cursor.fetchall()
    if len(result) != 0:
        base = Image.open("static/img/pps2.png").convert("RGBA")
        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
        fnt = ImageFont.truetype("arial.ttf", 30)
        fnt2 = ImageFont.truetype("arial.ttf", 27)
        d = ImageDraw.Draw(txt)
        y = 270
        count = 1
        for num in result:
            if str(num[3]) != "None":
                # id, name race, date, Машина, привод, покрытие, резина, время
                count += 1
                mpi = mpinfo(message, num[1])
                d.text((85, y), "№{} {}".format(num[1], mpi[1]), font=fnt2, fill=(0, 0, 0, 256))
                d.text((325, y), "{} {}".format(mpi[2], mpi[3]), font=fnt, fill=(0, 0, 0, 256))
                if len(num[4]) > 15:
                    count_c = 0
                    str_ncar = ""
                    for st in num[4]:
                         count_c += 1
                         str_ncar += str(st)
                         if count_c == 19:
                             str_ncar += '\n'

                    d.text((590, y), "{}".format(str_ncar), font=fnt, fill=(0, 0, 0, 256))
                else:
                    d.text((590, y), "{}".format(num[4]), font=fnt, fill=(0, 0, 0, 256))
                cari = carinfo(message, num[4])
                d.text((935, y), "{}".format(num[6]), font=fnt, fill=(0, 0, 0, 256))
                d.text((1190, y), "{}".format(mpi[4]), font=fnt, fill=(0, 0, 0, 256))
                d.text((1410, y), "{}".format(num[7]), font=fnt2, fill=(0, 0, 0, 256))
                d.text((1675, y), "{}".format(num[3]), font=fnt, fill=(0, 0, 0, 256))
                y += 100
        out = Image.alpha_composite(base, txt)
        if check == 3:
            if count > 1:
                #####
                #####
                bot.send_photo(message.chat.id, out, reply_markup=delb)
                bot.send_message(message.chat.id, "Выше на фото отображены *10 лучших* ваших результатов.", reply_markup=default_menu_user(), parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id, "Простите, результаты гонок не найдены, скорее всего их еще не внесли.", reply_markup=delb)
                bot.send_message(message.chat.id, "Вы вернулись в главное меню.", reply_markup=default_menu_user())
        elif check == 4:
            if count > 1:
                bot.send_photo(message.chat.id, out, reply_markup=delb)
                bot.send_message(message.chat.id, "Выше на фото отображены *10 лучших* ваших результатов.", reply_markup=default_menu_admin(), parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id, "Простите, результаты гонок не найдены, скорее всего их еще не внесли.", reply_markup=delb)
                bot.send_message(message.chat.id, "Вы вернулись в главное меню.", reply_markup=default_menu_admin())
    else:
        if check == 3:
            bot.send_message(message.chat.id, "Видимо вы еще не участвовали в гонках, или администратор не внёс результаты.", reply_markup=delb)
            bot.send_message(message.chat.id, "Вы вернулись в главное меню.", reply_markup=default_menu_user())
        elif check == 4:
            bot.send_message(message.chat.id, "Видимо вы еще не участвовали в гонках, или администратор не внёс результаты.", reply_markup=delb)
            bot.send_message(message.chat.id, "Вы вернулись в главное меню.", reply_markup=default_menu_admin())

def carinfo(message, carname):
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Cars (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, OwnerId INTEGER NOT NULL, Auto TEXT NOT NULL, RegPlate TEXT NOT NULL, Tyres TEXT NOT NULL, HP INTEGER NOT NULL, Weight INTEGER NOT NULL, EngineType TEXT NOT NULL, DriveUnit TEXT NOT NULL , TransmissionType TEXT NOT NULL)")
        cursor.execute("SELECT * FROM Cars WHERE OwnerId={} AND Auto='{}'".format(message.from_user.id, carname))
        conn.commit()
        car_info = cursor.fetchone()
    if str(car_info) == 'None':
        car_info = ('NOT\nFOUND', 'NOT\nFOUND', 'NOT\nFOUND', 'NOT\nFOUND', 'NOT\nFOUND', 'NOT\nFOUND', 'NOT\nFOUND', 'NOT\nFOUND', 'NOT\nFOUND', 'NOT\nFOUND')
    return car_info

def carinfo_all(chid, carname):
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Cars (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, OwnerId INTEGER NOT NULL, Auto TEXT NOT NULL, RegPlate TEXT NOT NULL, Tyres TEXT NOT NULL, HP INTEGER NOT NULL, Weight INTEGER NOT NULL, EngineType TEXT NOT NULL, DriveUnit TEXT NOT NULL , TransmissionType TEXT NOT NULL)")
        cursor.execute("SELECT * FROM Cars WHERE OwnerId={} AND Auto='{}'".format(chid, carname))
        conn.commit()
        car_info = cursor.fetchone()
    if str(car_info) == 'None':
        car_info = ('NOT\nFOUND', 'NOT\nFOUND', 'NOT\nFOUND', 'NOT\nFOUND', 'NOT\nFOUND', 'NOT\nFOUND', 'NOT\nFOUND', 'NOT\nFOUND', 'NOT\nFOUND', 'NOT\nFOUND')
    return car_info


def mpinfo(message, id):
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS MP (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpName TEXT NOT NULL, MpDate TEXT NOT NULL, MpTime TEXT NOT NULL, MpWeather TEXT NOT NULL, MpTemp INTEGER NOT NULL, MpMember INTEGER NOT NULL, MpMemberMax INTEGER NOT NULL, Status INTEGER NOT NULL)")
        cursor.execute("SELECT * FROM MP WHERE Id={}".format(id))
        conn.commit()
        mp_info = cursor.fetchone()
    if str(mp_info) == 'None':
        mp_info = ('NOT\nFOUND', 'NOT\nFOUND',  'NOT\nFOUND',  'NOT\nFOUND',  'NOT\nFOUND',  'NOT\nFOUND',  'NOT\nFOUND',  'NOT\nFOUND')
    return mp_info



def all_top_race(message):
    check = check_reg(message.chat.id)
    delb = telebot.types.ReplyKeyboardRemove()
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS MP_Result (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpId INTEGER NOT NULL, MpUserId INTEGER NOT NULL, Result FLOAT, UserCar TEXT NOT NULL, UStatus INTEGER NOT NULL, Privod TEXT, Rezina TEXT)")
        cursor.execute("SELECT * FROM MP_Result WHERE Ustatus=1 ORDER BY Result LIMIT 10")
        conn.commit()
    result = cursor.fetchall()
    if len(result) != 0:
        base = Image.open("static/img/top10all.png").convert("RGBA")
        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
        fnt = ImageFont.truetype("arial.ttf", 30)
        fnt2 = ImageFont.truetype("arial.ttf", 27)
        d = ImageDraw.Draw(txt)
        y = 270
        count = 1
        for num in result:
            if str(num[3]) != "None":
                # id, name race, date, Машина, привод, покрытие, резина, время
                count += 1
                mpi = mpinfo(message, num[1])
                d.text((85, y), "№{} {}".format(num[1], mpi[1]), font=fnt2, fill=(0, 0, 0, 256))
                d.text((325, y), "{} {}".format(mpi[2], mpi[3]), font=fnt, fill=(0, 0, 0, 256))
                # 590 , y
                usr = get_usr_info(num[2])
                d.text((590, y-10), "{}\n{}".format(usr[0], usr[1]), font=fnt, fill=(0, 0, 0, 256))
                if len(num[4]) > 15:
                    count_c = 0
                    str_ncar = ""
                    for st in num[4]:
                         count_c += 1
                         str_ncar += str(st)
                         if count_c == 19:
                             str_ncar += '\n'

                    d.text((880, y), "{}".format(str_ncar), font=fnt, fill=(0, 0, 0, 256))
                else:
                    d.text((880, y), "{}".format(num[4]), font=fnt, fill=(0, 0, 0, 256))
                cari = carinfo_all(num[2], num[4])
                d.text((1220, y), "{}".format(num[6]), font=fnt, fill=(0, 0, 0, 256))
                d.text((1470, y), "{}".format(mpi[4]), font=fnt, fill=(0, 0, 0, 256))
                d.text((1685, y), "{}".format(num[7]), font=fnt2, fill=(0, 0, 0, 256))
                d.text((1965, y), "{}".format(num[3]), font=fnt, fill=(0, 0, 0, 256))
                y += 100
        out = Image.alpha_composite(base, txt)
        if check == 3:
            if count > 1:
                #####
                #####
                bot.send_photo(message.chat.id, out, reply_markup=delb)
                bot.send_message(message.chat.id, "Выше на фото отображены *10 лучших* результатов всех гонщиков.", reply_markup=default_menu_user(), parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id, "Простите, результаты гонок не найдены, скорее всего их еще не внесли.", reply_markup=delb)
                bot.send_message(message.chat.id, "Вы вернулись в главное меню.", reply_markup=default_menu_user())
        elif check == 4:
            if count > 1:
                bot.send_photo(message.chat.id, out, reply_markup=delb)
                bot.send_message(message.chat.id, "Выше на фото отображены *10 лучших* результатов всех гонщиков.", reply_markup=default_menu_admin(), parse_mode="Markdown")
            else:
                bot.send_message(message.chat.id, "Простите, результаты гонок не найдены, скорее всего их еще не внесли.", reply_markup=delb)
                bot.send_message(message.chat.id, "Вы вернулись в главное меню.", reply_markup=default_menu_admin())
    else:
        if check == 3:
            bot.send_message(message.chat.id, "Видимо вы еще не участвовали в гонках, или администратор не внёс результаты.", reply_markup=delb)
            bot.send_message(message.chat.id, "Вы вернулись в главное меню.", reply_markup=default_menu_user())
        elif check == 4:
            bot.send_message(message.chat.id, "Видимо вы еще не участвовали в гонках, или администратор не внёс результаты.", reply_markup=delb)
            bot.send_message(message.chat.id, "Вы вернулись в главное меню.", reply_markup=default_menu_admin())

def get_usr_info(usrid):
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Users (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, FirstName TEXT NOT NULL, LastName TEXT NOT NULL, TGUserId INTEGER NOT NULL, MobilePhone NUMERIC NOT NULL, DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Status INTEGER NOT NULL DEFAULT 2, Alerts INTEGER NOT NULL DEFAULT 0)")
        cursor.execute("SELECT FirstName, LastName FROM Users WHERE TGUserId={}".format(usrid))
        conn.commit()
    result = cursor.fetchone()
    if str(result) == 'None':
        result = ('NOT FOUND', 'NOT FOUND')
    return result


def show_mp_menu(message):
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS MP (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpName TEXT NOT NULL, MpDate TEXT NOT NULL, MpTime TEXT NOT NULL, MpWeather TEXT NOT NULL, MpTemp INTEGER NOT NULL, MpMember INTEGER NOT NULL, MpMemberMax INTEGER NOT NULL, Status INTEGER NOT NULL)")
        cursor.execute("SELECT * FROM MP")
        result = cursor.fetchall()
        conn.commit()
    if len(result) > 0:
        mpbut = telebot.types.ReplyKeyboardMarkup(True, True)
        if len(result) >= 19:
            count = len(result)
            count -= 10
            count2 = 0
            for num in result:
                count2 += 1
                if count2 > count:
                    mpbut.row(' ID: {} | Name: {}\n Date: {} | Time: {}'.format(num[0], num[1], num[2], num[3]))
        else:
            for num in result:
                mpbut.row(' ID: {} | Name: {}\n Date: {} | Time: {}'.format(num[0], num[1], num[2], num[3]))
        mpbut.row('<< Назад')
        bot.send_message(message.from_user.id, "Здесь отображены крайние 10 мероприятий, для регистрации на них, выберите мероприятие.", reply_markup=mpbut)
        bot.register_next_step_handler(message, reg_user_mp)
    else:
        bot.send_message(message.from_user.id, "Простите, никаких мероприятий не запланировано в ближайшее время", reply_markup=mpbut)


def reg_user_mp(message):
    check = check_reg(message.from_user.id)
    delbut = telebot.types.ReplyKeyboardRemove()
    if message.text == "<< Назад":
        if check == 3:
            bot.send_message(message.from_user.id, "Вы вернулись в главное меню.", reply_markup=default_menu_user())
        elif check == 4:
            bot.send_message(message.from_user.id, "Вы вернулись в главное меню.", reply_markup=default_menu_admin())
    else:
        txt = message.text
        x = txt.split(" ")
        if len(x) >= 9:
            car_user_mp(message, x)
        else:
            bot.send_message(message.from_user.id, "Не пойму вас, такой кнопки нету, попробуйте еще раз.", reply_markup=delbut)
            show_mp_menu(message)

def car_user_mp(message, x):
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Cars (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, OwnerId INTEGER NOT NULL, Auto TEXT NOT NULL, RegPlate TEXT NOT NULL, Tyres TEXT NOT NULL, HP INTEGER NOT NULL, Weight INTEGER NOT NULL, EngineType TEXT NOT NULL, DriveUnit TEXT NOT NULL , TransmissionType TEXT NOT NULL)")
        cursor.execute("SELECT * FROM Cars WHERE OwnerId={}".format(message.from_user.id))
        conn.commit()
        result = cursor.fetchall()
    count = 0
    mycar = telebot.types.ReplyKeyboardMarkup(True, True)
    for num in result:
        mycar.row(str(num[2]))
        count +=1
    if count == 0:
        check = check_reg(message.from_user.id)
        if check == 3:
            bot.send_message(message.from_user.id, "В вашем гараже еще нет автомобилей. \nЧто-бы добавить, воспользуйтесь вкладкой: \n*'Мои автомобили'*.", parse_mode="Markdown", reply_markup=default_menu_user())
        elif check == 4:
            bot.send_message(message.from_user.id, "В вашем гараже еще нет автомобилей. \nЧто-бы добавить, воспользуйтесь вкладкой: \n*'Мои автомобили'*.", parse_mode="Markdown", reply_markup=default_menu_admin())
    else:
        bot.send_message(message.from_user.id, "В вашем гараже сейчас {} автомобиля(ей).\n\nВыберите авто на котором будете участвовать в гонке.".format(str(count)), parse_mode="Markdown", reply_markup=mycar)
        bot.register_next_step_handler(message, next_car_user_mp, x)


def next_car_user_mp(message, x):
    ncar = message.text
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Cars WHERE OwnerId={} AND Auto='{}'".format(message.from_user.id, ncar))
        n_tyres = cursor.fetchone()
        conn.commit()
    mytyres = telebot.types.ReplyKeyboardMarkup(True, True)
    mytyres.row('Да')
    mytyres.row('Нет')
    bot.send_message(message.from_user.id, "Скажите, на вашем авто осталась прежняя резина?\nНазвание: *{}*".format(n_tyres[4]), parse_mode="Markdown", reply_markup=mytyres)
    bot.register_next_step_handler(message, prefinish_car_user_mp, x, ncar)
    ####

def prefinish_car_user_mp(message, x, ncar):
    if message.text == 'Да':
        finish_car_user_mp(message, x, ncar)
    elif message.text == 'Нет':
        deltyr = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, "Укажите новое название вашей резины: ", reply_markup=deltyr)
        bot.register_next_step_handler(message, up_tyres, x, ncar)

def up_tyres(message, x, ncar):
    newtyres = message.text
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE Cars SET Tyres='{}' WHERE OwnerId={} AND Auto='{}'".format(newtyres, message.from_user.id, ncar))
        conn.commit()
    finish_car_user_mp(message, x, ncar)


def finish_car_user_mp(message, x, ncar):
    check = check_reg(message.from_user.id)
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM MP_Result WHERE (MpId={}) AND (MpUserId={})".format(x[1], message.from_user.id))
        result_info = cursor.fetchone()
        conn.commit()
    ####
    if result_info != None:
        if check == 3:
            bot.send_message(message.from_user.id, "Вы уже подали заявку на участие в данной гонке, ожидайте ответа администратора.", reply_markup=default_menu_user())
        elif check == 4:
            bot.send_message(message.from_user.id, "Вы уже подали заявку на участие в данной гонке, ожидайте ответа администратора.", reply_markup=default_menu_admin())
    else:
        insert_result_sql(message, x, ncar)
        if check == 3:
            bot.send_message(message.from_user.id, "Номер: *№{}*\nНазвание: *{}*Вы успешно зарегистрированы на гонку.\nДата проведения: *{}*\nВремя проведения: *{}*\nАвто: *{}*".format(x[1], x[4], x[6], x[9], ncar), reply_markup=default_menu_user(), parse_mode="Markdown")
        elif check == 4:
            bot.send_message(message.from_user.id, "Номер: *№{}*\nНазвание: *{}*Вы успешно зарегистрированы на гонку.\nДата проведения: *{}*\nВремя проведения: *{}*\nАвто: *{}*".format(x[1], x[4], x[6], x[9], ncar), reply_markup=default_menu_admin(), parse_mode="Markdown")

def insert_result_sql(message, x, ncar):
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Cars (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, OwnerId INTEGER NOT NULL, Auto TEXT NOT NULL, RegPlate TEXT NOT NULL, Tyres TEXT NOT NULL, HP INTEGER NOT NULL, Weight INTEGER NOT NULL, EngineType TEXT NOT NULL, DriveUnit TEXT NOT NULL , TransmissionType TEXT NOT NULL)")
        cursor.execute("SELECT * FROM Cars WHERE OwnerId={} AND Auto='{}'".format(message.from_user.id, ncar))
        car_info = cursor.fetchone()
        cursor.execute("CREATE TABLE IF NOT EXISTS MP_Result (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpId INTEGER NOT NULL, MpUserId INTEGER NOT NULL, Result FLOAT, UserCar TEXT NOT NULL, UStatus INTEGER NOT NULL, Privod TEXT, Rezina TEXT)")
        cursor.execute("INSERT INTO MP_Result (MpId, MpUserId, Result, UserCar, Ustatus, Privod, Rezina) values ('{}', '{}', NULL, '{}', 0, '{}', '{}')".format(x[1], message.from_user.id, ncar, car_info[7], car_info[4]))
        conn.commit()
    admins_send_mp_reg(message, x, ncar)

def admins_send_mp_reg(message, x, ncar):
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Users (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, FirstName TEXT NOT NULL, LastName TEXT NOT NULL, TGUserId INTEGER NOT NULL, MobilePhone NUMERIC NOT NULL, DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Status INTEGER NOT NULL DEFAULT 2, Alerts INTEGER NOT NULL DEFAULT 0)")
        cursor.execute("SELECT * FROM Users WHERE Status=4")
        result = cursor.fetchall()
        ###
        cursor.execute("SELECT * FROM Users WHERE TGUserId={}".format(message.from_user.id))
        uinfo = cursor.fetchone()
        ###
        conn.commit()

    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="Одобрить", callback_data="3")
    but_2 = types.InlineKeyboardButton(text="Отклонить", callback_data="4")
    key.add(but_1, but_2)
    for num in result:
        try:
            bot.send_message(num[3], "\[Запрос регистрации на гонку]\n TelegramChatID: *{}* \n Имя: *{}* \n Фамилия: *{}* \n МП: *{} - {}* Дата проведения: *{}* \n Время проведения: *{}* \n Авто: *{}*".format(message.from_user.id, uinfo[1], uinfo[2], x[1], x[4], x[6], x[9], ncar), reply_markup=key, parse_mode="Markdown")
        except:
            pass


def admin_panel(message):
    if message.text == 'Управление мероприятиями':
        bot.send_message(message.from_user.id, "Вы перешли в меню управления мероприятиями.", reply_markup=default_mp_action())
        bot.register_next_step_handler(message, menu_mp)
    elif message.text == 'Cписок запросов на регистрацию':
        testov(message)
    elif message.text == '<< Назад':
        bot.send_message(message.from_user.id, "Вы вернулись в главное меню.", reply_markup=default_menu_admin())

def menu_mp(message):
    if message.text == '<< Назад':
        bot.send_message(message.from_user.id, "Вы вернулись в панель управления администратора.", reply_markup=default_menu_admin_action())
        bot.register_next_step_handler(message, admin_panel)
    elif message.text == 'Список мероприятий':
        with sqlite3.connect("static/database/main.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS MP (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpName TEXT NOT NULL, MpDate TEXT NOT NULL, MpTime TEXT NOT NULL, MpWeather TEXT NOT NULL, MpTemp INTEGER NOT NULL, MpMember INTEGER NOT NULL, MpMemberMax INTEGER NOT NULL, Status INTEGER NOT NULL)")
            cursor.execute("SELECT * FROM MP")
            result = cursor.fetchall()
            conn.commit()

        if len(result) > 0:
            mpbut = telebot.types.ReplyKeyboardMarkup(True, True)
            if len(result) >= 19:
                count = len(result)
                count -= 10
                count2 = 0
                for num in result:
                    count2 += 1
                    if count2 > count:
                        mpbut.row(' ID: {} | Name: {} | Date: {} | Time: {}'.format(num[0], num[1], num[2], num[3]))
            else:
                for num in result:
                    mpbut.row(' ID: {} | Name: {} | Date: {} | Time: {}'.format(num[0], num[1], num[2], num[3]))
            mpbut.row('<< Назад')
            bot.send_message(message.from_user.id,"Здесь отображены крайние 10 мероприятий, для добавления результатов гонок выберите мероприятие.", reply_markup=mpbut)
            bot.register_next_step_handler(message, view_mp)
        else:
            bot.send_message(message.from_user.id, "Похоже что никаких мероприятий не проводиться.", reply_markup=default_mp_action())
            bot.register_next_step_handler(message, menu_mp)
    elif message.text == 'Добавить мероприятие':
        delbut = types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, "Для того что бы добавить мероприятие, следуйте инструкциям.", reply_markup=delbut)
        bot.send_message(message.from_user.id, "Введите название мероприятия: ")
        bot.register_next_step_handler(message, add_mp)

######################### закончил тут
def view_mp(message):
    if message.text == '<< Назад':
        bot.send_message(message.from_user.id, 'Вы вернулись в меню управления мероприятиями.', reply_markup=default_mp_action())
    else:
        txt = message.text
        x = txt.split(" ")
        if len(x) >= 11:
            #print(x)
            with sqlite3.connect("static/database/main.sqlite") as conn:
                cursor = conn.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS MP (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpName TEXT NOT NULL, MpDate TEXT NOT NULL, MpTime TEXT NOT NULL, MpWeather TEXT NOT NULL, MpTemp INTEGER NOT NULL, MpMember INTEGER NOT NULL, MpMemberMax INTEGER NOT NULL, Status INTEGER NOT NULL)")
                cursor.execute("SELECT * FROM MP WHERE Id={} AND MpName='{}' AND MpDate='{}'".format(x[1], x[4], x[7]))
                checkmp = cursor.fetchone()
                conn.commit()
            if checkmp != None:
                delmp = telebot.types.ReplyKeyboardMarkup(True, True)
                delmp.row('Подробная информация')
                delmp.row('ВНЕСТИ РЕЗУЛЬТАТЫ')
                delmp.row('Редактировать информацию')
                delmp.row('Оповестить о результатах')
                delmp.row('<< Назад')
                bot.send_message(message.from_user.id, 'Воспользуйтесь меню для выбора действия.', reply_markup=delmp)
                bot.register_next_step_handler(message, action_mp, checkmp)
        else:
            bot.send_message(message.from_user.id, 'Такое мероприятие не найдено, возможно его не существует.', reply_markup=default_mp_action())
            bot.register_next_step_handler(message, menu_mp)


def action_mp(message, checkmp):
    mm = telebot.types.ReplyKeyboardMarkup(True, True)
    mm.row('Подробная информация')
    mm.row('ВНЕСТИ РЕЗУЛЬТАТЫ')
    mm.row('Редактировать информацию')
    mm.row('Оповестить о результатах')
    mm.row('<< Назад')
    if message.text == 'Подробная информация':
        bot.send_message(message.from_user.id, '(----Подробная информация----)\nID: *{}*\nНазвание: *{}*\nДата: *{}*\nВремя: *{}*\nПокрытие: *{}*\nТемпература: *{}*\nМакс. кол-во участников: *{}*\nКол-во участников: *{}*\n'.format(checkmp[0], checkmp[1], checkmp[2], checkmp[3], checkmp[4], checkmp[5], checkmp[6], checkmp[7]), reply_markup=mm, parse_mode="Markdown")
        bot.register_next_step_handler(message, action_mp, checkmp)
    elif message.text == 'ВНЕСТИ РЕЗУЛЬТАТЫ':
        insert_result(message, checkmp)
    elif message.text == 'Редактировать информацию':
        edit_mp(message, checkmp)
    elif message.text == 'Оповестить о результатах':
        alert_mp(message, checkmp)
    elif message.text == '<< Назад':
        bot.send_message(message.from_user.id, 'Вы вернулись назад.', reply_markup=default_mp_action())
        bot.register_next_step_handler(message, menu_mp)
    else:
        bot.send_message(message.from_user.id, 'Не понимаю о чем вы, видимо ошиблись.', reply_markup=default_mp_action())
        bot.register_next_step_handler(message, menu_mp)


def insert_result(message, checkmp):
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS MP_Result (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpId INTEGER NOT NULL, MpUserId INTEGER NOT NULL, Result FLOAT NOT NULL, UserCar TEXT NOT NULL, UStatus INTEGER NOT NULL)")
        cursor.execute("SELECT * FROM MP_Result WHERE MpId={} AND Ustatus=1".format(checkmp[0]))
        conn.commit()
        users_insert = cursor.fetchall()
    if len(users_insert) == 1:
        pass
    elif len(users_insert) > 1:
        mm = telebot.types.ReplyKeyboardMarkup(True, True)
        for num in users_insert:
            info = getnameusr(num)
            mm.row('{} | {} {} | {}'.format(num[2], info[1], info[2], num[4]))
        mm.row('<< Назад')
        bot.send_message(message.from_user.id, 'Для внесения результатов гонки, выберите участника.', reply_markup=mm)
        bot.register_next_step_handler(message, result_race, checkmp)
    else:
        mm = telebot.types.ReplyKeyboardMarkup(True, True)
        mm.row('Подробная информация')
        mm.row('ВНЕСТИ РЕЗУЛЬТАТЫ')
        mm.row('Редактировать информацию')
        mm.row('Оповестить о результатах')
        mm.row('<< Назад')
        bot.send_message(message.from_user.id, 'На это мероприятие нет зарегистрированных участников. ', reply_markup=mm)
        bot.register_next_step_handler(message, action_mp, checkmp)

def result_race(message, checkmp):
    if message.text == '<< Назад':
        mm = telebot.types.ReplyKeyboardMarkup(True, True)
        mm.row('Подробная информация')
        mm.row('ВНЕСТИ РЕЗУЛЬТАТЫ')
        mm.row('Редактировать информацию')
        mm.row('Оповестить о результатах')
        mm.row('<< Назад')
        bot.send_message(message.from_user.id, 'Вы вернулись в меню выбора действий. ', reply_markup=mm)
        bot.register_next_step_handler(message, action_mp, checkmp)
    else:
        x = message.text.split(" | ")
        mm = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, 'Гонщик: *{}*\nАвто: *{}*\nУкажите значение результа заезда в формате - 0:00,000.\nПример: *1:23,220* или *0:01,000*'.format(x[1], x[2]), reply_markup=mm, parse_mode="Markdown")
        bot.register_next_step_handler(message, next_result_race, checkmp, x)


def next_result_race(message, checkmp, x):
    a = re.search("^[0-9]:[0-9][0-9],[0-9][0-9][0-9]$", message.text)
    b = re.search("^[0-9][0-9]:[0-9][0-9],[0-9][0-9][0-9]$", message.text)
    if a or b:
        with sqlite3.connect("static/database/main.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS MP_Result (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpId INTEGER NOT NULL, MpUserId INTEGER NOT NULL, Result FLOAT NOT NULL, UserCar TEXT NOT NULL, UStatus INTEGER NOT NULL)")
            cursor.execute("UPDATE MP_Result SET Result='{}' WHERE MpId={} AND Ustatus=1 AND MpUserId={}".format(message.text, checkmp[0], x[0]))
            conn.commit()
        bot.send_message(message.from_user.id, "Результат - *{}* для *{} | {}* был успешно записан.".format(message.text, x[1], x[2]), parse_mode="Markdown")
        insert_result(message, checkmp)
    else:
        bot.send_message(message.from_user.id, "Вы указали неверное значение, пожалуйста укажите в формате *0:00,000* или *00:00,000*\nВведите значение: ", parse_mode="Markdown")
        bot.register_next_step_handler(message, next_result_race, checkmp, x)


def getnameusr(num):
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Users (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, FirstName TEXT NOT NULL, LastName TEXT NOT NULL, TGUserId INTEGER NOT NULL, MobilePhone NUMERIC NOT NULL, DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Status INTEGER NOT NULL DEFAULT 2, Alerts INTEGER NOT NULL DEFAULT 0)")
        cursor.execute("SELECT * FROM Users WHERE (Status=3 OR Status=4) AND TGUserId={}".format(num[2]))
        conn.commit()
        result = cursor.fetchone()
    return result


def edit_mp(message, checkmp):
    mm = telebot.types.ReplyKeyboardMarkup(True, True)
    mm.row('Название')
    mm.row('Дата проведения')
    mm.row('Время проведения')
    mm.row('Покрытие')
    mm.row('Температура')
    mm.row('Максимальное кол-во участников')
    mm.row('<< Назад')
    bot.send_message(message.from_user.id, 'Пожалуйста, выберите поле которое хотите отредактировать. ', reply_markup=mm)
    bot.register_next_step_handler(message, edit_mp_action, checkmp)

def edit_mp_action(message, checkmp):
    delut = telebot.types.ReplyKeyboardRemove()
    if message.text == 'Название':
        bot.send_message(message.from_user.id, 'Укажите новое название мероприятия: ')
        bot.register_next_step_handler(message, name_mp, checkmp)
    elif message.text == 'Дата проведения':
        bot.send_message(message.from_user.id, 'Укажите новую дату проведения мероприятия: ')
        bot.register_next_step_handler(message, date_mp, checkmp)
    elif message.text == 'Время проведения':
        bot.send_message(message.from_user.id, 'Укажите новое время проведения мероприятия: ')
        bot.register_next_step_handler(message, time_mp, checkmp)
    elif message.text == 'Покрытие':
        bot.send_message(message.from_user.id, 'Укажите новое покрытие трассы (погодные условия): ')
        bot.register_next_step_handler(message, weather_mp, checkmp)
    elif message.text == 'Температура':
        bot.send_message(message.from_user.id, 'Укажите новую температуру воздуха: ')
        bot.register_next_step_handler(message, temp_mp, checkmp)
    elif message.text == 'Максимальное кол-во участников':
        bot.send_message(message.from_user.id, 'Укажите новое число участников: ')
        bot.register_next_step_handler(message, member_mp, checkmp)
    elif message.text == '<< Назад':
        delmp = telebot.types.ReplyKeyboardMarkup(True, True)
        delmp.row('Подробная информация')
        delmp.row('ВНЕСТИ РЕЗУЛЬТАТЫ')
        delmp.row('Редактировать информацию')
        delmp.row('Оповестить о результатах')
        delmp.row('<< Назад')
        bot.send_message(message.from_user.id, 'Воспользуйтесь меню для выбора действия.', reply_markup=delmp)
        bot.register_next_step_handler(message, action_mp, checkmp)


def alert_mp(message, checkmp):
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS MP_Result (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpId INTEGER NOT NULL, MpUserId INTEGER NOT NULL, Result FLOAT NOT NULL, UserCar TEXT NOT NULL, UStatus INTEGER NOT NULL)")
        cursor.execute("SELECT * FROM MP_Result WHERE MpId={} AND Ustatus=1".format(checkmp[0]))
        conn.commit()
        users_alert = cursor.fetchall()
    count_a = 0
    if len(users_alert) > 1:
        for num in users_alert:
            if num[3] != None:
                try:
                    count_a += 1
                    bot.send_message(num[2], "Мероприятие: №{} {} завершено. \n(*{} {}*)\n\nВаши результаты\nАвто: *{}*\nРезина: *{}*\nПривод: *{}*\nВремя (результат): *{}*".format(checkmp[0], checkmp[1], checkmp[2], checkmp[3], num[4], num[7], num[6], num[3]), parse_mode="Markdown")
                except:
                    pass
        ####
        mm = telebot.types.ReplyKeyboardMarkup(True, True)
        mm.row('Подробная информация')
        mm.row('ВНЕСТИ РЕЗУЛЬТАТЫ')
        mm.row('Редактировать информацию')
        mm.row('Оповестить о результатах')
        mm.row('<< Назад')
        bot.send_message(message.from_user.id, 'Было оповещено *{}* участников.\nВоспользуйтесь меню для выбора действия.'.format(count_a), reply_markup=mm, parse_mode="Markdown")
        bot.register_next_step_handler(message, action_mp, checkmp)
        ####
    elif len(users_alert) == 1:
        if users_alert[3] != None:
            ###
            bot.send_message(users_alert[2],"Мероприятие: №{} {} завершено. \n(*{} {}*)\n\nВаши результаты\nАвто: *{}*\nРезина: *{}*\nПривод: *{}*\nВремя (результат): *{}*".format(checkmp[0], checkmp[1], checkmp[2], checkmp[3], users_alert[4], users_alert[7], users_alert[6], users_alert[3]), parse_mode="Markdown")
            ###
            mm = telebot.types.ReplyKeyboardMarkup(True, True)
            mm.row('Подробная информация')
            mm.row('ВНЕСТИ РЕЗУЛЬТАТЫ')
            mm.row('Редактировать информацию')
            mm.row('Оповестить о результатах')
            mm.row('<< Назад')
            bot.send_message(message.from_user.id, 'Был оповещен *1* участник.\nВоспользуйтесь меню для выбора действия.', reply_markup=mm, parse_mode="Markdown")
            bot.register_next_step_handler(message, action_mp, checkmp)
    else:
        mm = telebot.types.ReplyKeyboardMarkup(True, True)
        mm.row('Подробная информация')
        mm.row('ВНЕСТИ РЕЗУЛЬТАТЫ')
        mm.row('Редактировать информацию')
        mm.row('Оповестить о результатах')
        mm.row('<< Назад')
        bot.send_message(message.from_user.id, 'Видимо возникла какая-то ошибка, возможно еще не внесены результаты.\nВоспользуйтесь меню для выбора действия.', reply_markup=mm)
        bot.register_next_step_handler(message, action_mp, checkmp)


def name_mp(message, checkmp):
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS MP (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpName TEXT NOT NULL, MpDate TEXT NOT NULL, MpTime TEXT NOT NULL, MpWeather TEXT NOT NULL, MpTemp INTEGER NOT NULL, MpMember INTEGER NOT NULL, MpMemberMax INTEGER NOT NULL, Status INTEGER NOT NULL)")
        cursor.execute("UPDATE MP SET MpName='{}' WHERE Id={} AND MpName='{}'".format(message.text, checkmp[0], checkmp[1]))
        conn.commit()
    bot.send_message(message.from_user.id, 'Название мероприятия было изменено на: *{}*'.format(message.text), parse_mode="Markdown")
    edit_mp(message, checkmp)

def date_mp(message, checkmp):
    mp_date = message.text
    x = re.search("^[0-9][0-9].[0-9][0-9].[0-9][0-9][0-9][0-9]$", mp_date)
    if x:
        with sqlite3.connect("static/database/main.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS MP (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpName TEXT NOT NULL, MpDate TEXT NOT NULL, MpTime TEXT NOT NULL, MpWeather TEXT NOT NULL, MpTemp INTEGER NOT NULL, MpMember INTEGER NOT NULL, MpMemberMax INTEGER NOT NULL, Status INTEGER NOT NULL)")
            cursor.execute("UPDATE MP SET MpDate='{}' WHERE Id={} AND MpName='{}'".format(message.text, checkmp[0], checkmp[1]))
            conn.commit()
        bot.send_message(message.from_user.id, 'Дата проведения мероприятия была изменено на: *{}*'.format(message.text), parse_mode="Markdown")
        edit_mp(message, checkmp)
    else:
        bot.send_message(message.from_user.id, "Вы указали дату в неверном формате.\nПример форматов:\n*21.09.2021*\n*21.11.2021*\n*09.09.2021*\n\nУкажите правильный формат: ", parse_mode="Markdown")
        bot.register_next_step_handler(message, date_mp, checkmp)


def time_mp(message, checkmp):
    mp_time = message.text
    x = re.search("^[0-9][0-9]:[0-9][0-9]$", mp_time)
    if x:
        with sqlite3.connect("static/database/main.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS MP (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpName TEXT NOT NULL, MpDate TEXT NOT NULL, MpTime TEXT NOT NULL, MpWeather TEXT NOT NULL, MpTemp INTEGER NOT NULL, MpMember INTEGER NOT NULL, MpMemberMax INTEGER NOT NULL, Status INTEGER NOT NULL)")
            cursor.execute("UPDATE MP SET MpTime='{}' WHERE Id={} AND MpName='{}'".format(message.text, checkmp[0], checkmp[1]))
            conn.commit()
        bot.send_message(message.from_user.id, 'Время проведения мероприятия было изменено на: *{}*'.format(message.text), parse_mode="Markdown")
        edit_mp(message, checkmp)
    else:
        bot.send_message(message.from_user.id, "Вы указали время в неверном формате.\nПример форматов:\n*09:00*\n*09:11*\n*10:09*\n\nУкажите правильный формат: ", parse_mode="Markdown")
        bot.register_next_step_handler(message, time_mp, checkmp)


def weather_mp(message, checkmp):
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS MP (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpName TEXT NOT NULL, MpDate TEXT NOT NULL, MpTime TEXT NOT NULL, MpWeather TEXT NOT NULL, MpTemp INTEGER NOT NULL, MpMember INTEGER NOT NULL, MpMemberMax INTEGER NOT NULL, Status INTEGER NOT NULL)")
        cursor.execute("UPDATE MP SET MpWeather='{}' WHERE Id={} AND MpName='{}'".format(message.text, checkmp[0], checkmp[1]))
        conn.commit()
    bot.send_message(message.from_user.id, 'Покрытие (погодные условия) было изменено на: *{}*'.format(message.text), parse_mode="Markdown")
    edit_mp(message, checkmp)


def temp_mp(message, checkmp):
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS MP (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpName TEXT NOT NULL, MpDate TEXT NOT NULL, MpTime TEXT NOT NULL, MpWeather TEXT NOT NULL, MpTemp INTEGER NOT NULL, MpMember INTEGER NOT NULL, MpMemberMax INTEGER NOT NULL, Status INTEGER NOT NULL)")
        cursor.execute("UPDATE MP SET MpTemp='{}' WHERE Id={} AND MpName='{}'".format(message.text, checkmp[0], checkmp[1]))
        conn.commit()
    bot.send_message(message.from_user.id, 'Температура была изменена на: *{}*'.format(message.text), parse_mode="Markdown")
    edit_mp(message, checkmp)


def member_mp(message, checkmp):
    member = message.text
    x = re.search("^[0-9]$", member)
    y = re.search("^[0-9][0-9]$", member)
    z = re.search("^[0-9][0-9][0-9]$", member)
    if x or y or z:
        with sqlite3.connect("static/database/main.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS MP (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpName TEXT NOT NULL, MpDate TEXT NOT NULL, MpTime TEXT NOT NULL, MpWeather TEXT NOT NULL, MpTemp INTEGER NOT NULL, MpMember INTEGER NOT NULL, MpMemberMax INTEGER NOT NULL, Status INTEGER NOT NULL)")
            cursor.execute("UPDATE MP SET MpMember='{}' WHERE Id={} AND MpName='{}'".format(message.text, checkmp[0], checkmp[1]))
            conn.commit()
        bot.send_message(message.from_user.id, 'Максимальное кол-во участников было изменено на: *{}*'.format(message.text), parse_mode="Markdown")
        edit_mp(message, checkmp)
    else:
        bot.send_message(message.from_user.id, "Количество участников может варироватся от 0 до 999 участников.\n\nУкажите правильный формат: ", parse_mode="Markdown")
        bot.register_next_step_handler(message, member_mp, checkmp)


def add_mp(message):
    mp_name = message.text
    bot.send_message(message.from_user.id, "Укажите дату проведения\n(пример 29.01.2021): ")
    bot.register_next_step_handler(message, add_mp_date, mp_name)

def add_mp_date(message, mp_name):
    mp_date = message.text
    x = re.search("^[0-9][0-9].[0-9][0-9].[0-9][0-9][0-9][0-9]$", mp_date)
    if x:
        bot.send_message(message.from_user.id, "Укажите время проведения\n(например - 15:00): ")
        bot.register_next_step_handler(message, add_mp_time, mp_name, mp_date)
    else:
        bot.send_message(message.from_user.id, "Вы указали дату в неверном формате.\nПример форматов:\n*21.09.2021*\n*21.11.2021*\n*09.09.2021*\n\nУкажите правильный формат: ", parse_mode="Markdown")
        bot.register_next_step_handler(message, add_mp_date, mp_name)


def add_mp_time(message, mp_name, mp_date):
    mp_time = message.text
    x = re.search("^[0-9][0-9]:[0-9][0-9]$", mp_time)
    if x:
        bot.send_message(message.from_user.id, "Укажите погодные условия: ")
        bot.register_next_step_handler(message, add_mp_weather, mp_name, mp_date, mp_time)
    else:
        bot.send_message(message.from_user.id, "Вы указали время в неверном формате.\nПример форматов:\n*09:00*\n*09:11*\n*10:09*\n\nУкажите правильный формат: ", parse_mode="Markdown")
        bot.register_next_step_handler(message, add_mp_time, mp_name, mp_date)


def add_mp_weather(message, mp_name, mp_date, mp_time):
    mp_weather = message.text
    bot.send_message(message.from_user.id, "Укажите температуру воздуха: ")
    bot.register_next_step_handler(message, add_mp_temp, mp_name, mp_date, mp_time, mp_weather)

def add_mp_temp(message, mp_name, mp_date, mp_time, mp_weather):
    mp_temp = message.text
    bot.send_message(message.from_user.id, "Укажите количество участников: ")
    bot.register_next_step_handler(message, add_mp_member, mp_name, mp_date, mp_time, mp_weather, mp_temp)

def add_mp_member(message, mp_name, mp_date, mp_time, mp_weather, mp_temp):
    mp_member = message.text
    x = re.search("^[0-9]$", mp_member)
    y = re.search("^[0-9][0-9]$", mp_member)
    z = re.search("^[0-9][0-9][0-9]$", mp_member)
    if x or y or z:
        insert_sql_mp(message, mp_name, mp_date, mp_time, mp_weather, mp_temp, mp_member)
    else:
        bot.send_message(message.from_user.id, "Используйте число для указания количества участников (от 0 до 999): ")
        bot.register_next_step_handler(message, add_mp_member, mp_name, mp_date, mp_time, mp_weather, mp_temp)

def insert_sql_mp(message, mp_name, mp_date, mp_time, mp_weather, mp_temp, mp_member):
    create_mp = "Мероприятие *'{}'*\nуспешно создано.\n*Дата проведения:* {}\n*Время проведения:* {}\n*Покрытие:* {}\n*Температура:* {}\n*Макс. кол-во участников:* {}\n".format(mp_name, mp_date, mp_time, mp_weather, mp_temp, mp_member)
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS MP (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpName TEXT NOT NULL, MpDate TEXT NOT NULL, MpTime TEXT NOT NULL, MpWeather TEXT NOT NULL, MpTemp INTEGER NOT NULL, MpMember INTEGER NOT NULL, MpMemberMax INTEGER NOT NULL, Status INTEGER NOT NULL)")
        cursor.execute("INSERT INTO MP (MpName, MpDate, MpTime, MpWeather, MpTemp, MpMember, MpMemberMax, Status) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(mp_name, mp_date, mp_time, mp_weather, mp_temp, mp_member, 0, 0))
        conn.commit()
    bot.send_message(message.from_user.id, create_mp, parse_mode="Markdown", reply_markup=default_mp_action())
    send_all_mp_create(mp_name, mp_date, mp_time, mp_weather, mp_temp, mp_member)
    bot.register_next_step_handler(message, menu_mp)

def send_all_mp_create(mp_name, mp_date, mp_time, mp_weather, mp_temp, mp_member):
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Users (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, FirstName TEXT NOT NULL, LastName TEXT NOT NULL, TGUserId INTEGER NOT NULL, MobilePhone NUMERIC NOT NULL, DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Status INTEGER NOT NULL DEFAULT 2, Alerts INTEGER NOT NULL DEFAULT 0)")
        cursor.execute("SELECT * FROM Users WHERE (Status=3 OR Status=4) AND Alerts=0")
        conn.commit()
        result = cursor.fetchall()
    create_mp = "Администратор создал мероприятие *'{}'*\n*Дата проведения:* {}\n*Время проведения:* {}\n*Покрытие:* {}\n*Температура:* {}\n*Макс. кол-во участников:* {}\nВы можете принять участие, регистрируйтесь!".format(mp_name, mp_date, mp_time, mp_weather, mp_temp, mp_member)
    if str(result) != 'None':
        if len(result) > 1:
            for num in result:
                try:
                    bot.send_message(num[3], create_mp, parse_mode="Markdown")
                except:
                    pass
        else:
            try:
                bot.send_message(result[3], create_mp, parse_mode="Markdown")
            except:
                pass

def get_car_user(message):
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Cars (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, OwnerId INTEGER NOT NULL, Auto TEXT NOT NULL, RegPlate TEXT NOT NULL, Tyres TEXT NOT NULL, HP INTEGER NOT NULL, Weight INTEGER NOT NULL, EngineType TEXT NOT NULL, DriveUnit TEXT NOT NULL , TransmissionType TEXT NOT NULL)")
        cursor.execute("SELECT * FROM Cars WHERE OwnerId={}".format(message.from_user.id))
        conn.commit()
        result = cursor.fetchall()
    count = 0
    mycar = telebot.types.ReplyKeyboardMarkup(True, True)
    for num in result:
        mycar.row(str(num[2]))
        count += 1
    mycar.row('Добавить автомобиль')
    mycar.row('<< Назад')
    if count == 0:
        check = check_reg(message.from_user.id)
        if check == 3:
            bot.send_message(message.from_user.id, "В вашем гараже еще нет автомобилей. \nВоспользуйтесь кнопкой: \n*'Добавить автомобиль'*.", parse_mode="Markdown", reply_markup=mycar)
            bot.register_next_step_handler(message, next_car_action)
        elif check == 4:
            bot.send_message(message.from_user.id, "В вашем гараже еще нет автомобилей. \nВоспользуйтесь кнопкой: \n*'Добавить автомобиль'*.", parse_mode="Markdown", reply_markup=mycar)
            bot.register_next_step_handler(message, next_car_action)
    else:
        bot.send_message(message.from_user.id, "В вашем гараже сейчас {} автомобиля(ей), для управления выберите автомобиль. \n\nЕсли хотите добавить новый, используйте кнопку: \n*'Добавить автомобиль'*".format(str(count)), parse_mode="Markdown", reply_markup=mycar)
        bot.register_next_step_handler(message, next_car_action)


def next_hop(message):
    carbut = types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, "Что бы добавить автомобиль в гараж, следуйте дальнейшим инструкциям бота.", reply_markup=carbut)
    ownerid = message.from_user.id
    bot.send_message(message.from_user.id, "Введите название марки авто и модель: ")
    bot.register_next_step_handler(message, get_car_name, ownerid)


def next_car_action(message):
    namecaraction = message.text
    check = check_reg(message.from_user.id)
    if check == 3:
        if message.text == "Добавить автомобиль":
            next_hop(message)
        elif message.text == "<< Назад":
            bot.send_message(message.from_user.id, "Вы вернулись в главное меню.", reply_markup=default_menu_user())
        else:
            caredit = telebot.types.ReplyKeyboardMarkup(True, True)
            caredit.row("Редактировать данные")
            caredit.row("Посмотреть ТТХ")
            caredit.row("Удалить автомобиль")
            caredit.row("<< Назад ")
            bot.send_message(message.from_user.id, "Вы выбрали: {}\nИспользуйте меню для выбора действий.".format(namecaraction), reply_markup=caredit)
            bot.register_next_step_handler(message, car_edit_menu, namecaraction)
    elif check == 4:
        if message.text == "Добавить автомобиль":
            next_hop(message)
        elif message.text == "<< Назад":
            bot.send_message(message.from_user.id, "Вы вернулись в главное меню.", reply_markup=default_menu_admin())
        else:
            caredit = telebot.types.ReplyKeyboardMarkup(True, True)
            caredit.row("Редактировать данные")
            caredit.row("Посмотреть ТТХ")
            caredit.row("Удалить автомобиль")
            caredit.row("<< Назад ")
            bot.send_message(message.from_user.id, "Вы выбрали: *{}*\nИспользуйте меню для выбора действий.".format(namecaraction), reply_markup=caredit, parse_mode="Markdown")
            bot.register_next_step_handler(message, car_edit_menu, namecaraction)

def car_edit_menu(message, namecaraction):
    if message.text == 'Редактировать данные':
        caredit_usr = telebot.types.ReplyKeyboardMarkup(True, True)
        caredit_usr.row('Название и модель')
        caredit_usr.row('Номерной знак')
        caredit_usr.row('Название резины')
        caredit_usr.row('Лошадиные силы')
        caredit_usr.row('Вес')
        caredit_usr.row('Привод')
        caredit_usr.row('Тип двигателя')
        caredit_usr.row('Трансмиссия')
        caredit_usr.row('<< Назад')
        bot.send_message(message.chat.id, "Пожалуйста, используйте меню для выбора даных, которые вы хотите отредактировать.", parse_mode="Markdown", reply_markup=caredit_usr)
        bot.register_next_step_handler(message, next_action_edits_car, namecaraction)
        #get_car_user(message)
    elif message.text == 'Посмотреть ТТХ':
        with sqlite3.connect("static/database/main.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Cars (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, OwnerId INTEGER NOT NULL, Auto TEXT NOT NULL, RegPlate TEXT NOT NULL, Tyres TEXT NOT NULL, HP INTEGER NOT NULL, Weight INTEGER NOT NULL, EngineType TEXT NOT NULL, DriveUnit TEXT NOT NULL , TransmissionType TEXT NOT NULL)")
            cursor.execute("SELECT * FROM Cars WHERE OwnerId={} AND Auto='{}'".format(message.chat.id, namecaraction))
            conn.commit()
            car_result = cursor.fetchone()
        ##
        bot.send_message(message.chat.id, "----(CAR INFO)----\nНазвание: *{}*\nНомер: *{}*\nРезина: *{}*\nЛош. силы: *{}*\nВес: *{}*\nПривод: *{}*\nТип двигателя: *{}*\nТрансмиссия: *{}*\n".format(car_result[2], car_result[3], car_result[4], car_result[5], car_result[6], car_result[7], car_result[8], car_result[9]), parse_mode="Markdown")
        get_car_user(message)
    elif message.text == 'Удалить автомобиль':
        ##
        with sqlite3.connect("static/database/main.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Cars (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, OwnerId INTEGER NOT NULL, Auto TEXT NOT NULL, RegPlate TEXT NOT NULL, Tyres TEXT NOT NULL, HP INTEGER NOT NULL, Weight INTEGER NOT NULL, EngineType TEXT NOT NULL, DriveUnit TEXT NOT NULL , TransmissionType TEXT NOT NULL)")
            cursor.execute("DELETE FROM Cars WHERE OwnerId={} AND Auto='{}'".format(message.chat.id, namecaraction))
            conn.commit()
        ##
        bot.send_message(message.chat.id, "Вы удалили авто: *{}*\nиз своего виртуального гаража.".format(namecaraction), parse_mode="Markdown")
        get_car_user(message)
    elif message.text == '<< Назад':
        get_car_user(message)
    else:
        bot.send_message(message.chat.id, "Вы видимо ошиблись в выборе действия, попробуйте еще раз.")
        get_car_user(message)
### блок общения для регистрации
#####



def next_action_edits_car(message, namecaraction):
    caredit_usr = telebot.types.ReplyKeyboardRemove()
    if message.text == 'Название и модель':
        bot.send_message(message.chat.id, "Пожалуйста, укажите новое название и модель авто:", reply_markup=caredit_usr)
        bot.register_next_step_handler(message, change_name_car, namecaraction)
    elif message.text == 'Номерной знак':
        bot.send_message(message.chat.id, "Пожалуйста, укажите новый номерной знак:", reply_markup=caredit_usr)
        bot.register_next_step_handler(message, change_reg_car, namecaraction)
    elif message.text == 'Название резины':
        bot.send_message(message.chat.id, "Пожалуйста, укажите новое название резины:", reply_markup=caredit_usr)
        bot.register_next_step_handler(message, change_tyres_car, namecaraction)
    elif message.text == 'Лошадиные силы':
        bot.send_message(message.chat.id, "Пожалуйста, укажите новое значение лошадиных сил (числом):", reply_markup=caredit_usr)
        bot.register_next_step_handler(message, change_hp_car, namecaraction)
    elif message.text == 'Вес':
        bot.send_message(message.chat.id, "Пожалуйста, укажите новое значение веса авто (числом):", reply_markup=caredit_usr)
        bot.register_next_step_handler(message, change_weight_car, namecaraction)
    elif message.text == 'Привод':
        tranv = telebot.types.ReplyKeyboardMarkup(True, True)
        tranv.row('Полный')
        tranv.row('Передний')
        tranv.row('Задний')
        bot.send_message(message.chat.id, "Пожалуйста, укажите привод авто:", reply_markup=tranv)
        bot.register_next_step_handler(message, change_engine_car, namecaraction)
    elif message.text == 'Тип двигателя':
        tranv = telebot.types.ReplyKeyboardMarkup(True, True)
        tranv.row('Бензиновый')
        tranv.row('Дизельный')
        tranv.row('Электро')
        bot.send_message(message.chat.id, "Пожалуйста, укажите тип двигателя:", reply_markup=tranv)
        bot.register_next_step_handler(message, change_drive_car, namecaraction)
    elif message.text == 'Трансмиссия':
        tranv = telebot.types.ReplyKeyboardMarkup(True, True)
        tranv.row('Автомат')
        tranv.row('Механика')
        tranv.row('Робот')
        bot.send_message(message.chat.id, "Пожалуйста, укажите тип трансмисии:", reply_markup=tranv)
        bot.register_next_step_handler(message, change_trans_car, namecaraction)
    elif message.text == '<< Назад':
        get_car_user(message)


def change_name_car(message, namecaraction):
    newcarname = message.text
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Cars (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, OwnerId INTEGER NOT NULL, Auto TEXT NOT NULL, RegPlate TEXT NOT NULL, Tyres TEXT NOT NULL, HP INTEGER NOT NULL, Weight INTEGER NOT NULL, EngineType TEXT NOT NULL, DriveUnit TEXT NOT NULL , TransmissionType TEXT NOT NULL)")
        cursor.execute("UPDATE Cars SET Auto='{}' WHERE Auto='{}' AND OwnerId={}".format(newcarname, namecaraction, message.chat.id))
        conn.commit()
    bot.send_message(message.from_user.id, 'Название автомобиля было изменено на: *{}*'.format(newcarname), parse_mode="Markdown")
    get_car_user(message)


def change_reg_car(message, namecaraction):
    newreg = message.text
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Cars (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, OwnerId INTEGER NOT NULL, Auto TEXT NOT NULL, RegPlate TEXT NOT NULL, Tyres TEXT NOT NULL, HP INTEGER NOT NULL, Weight INTEGER NOT NULL, EngineType TEXT NOT NULL, DriveUnit TEXT NOT NULL , TransmissionType TEXT NOT NULL)")
        cursor.execute("UPDATE Cars SET RegPlate='{}' WHERE Auto='{}' AND OwnerId={}".format(newreg, namecaraction, message.chat.id))
        conn.commit()
    bot.send_message(message.from_user.id, 'Номерной знак автомобиля был изменен на: *{}*'.format(newreg), parse_mode="Markdown")
    get_car_user(message)


def change_tyres_car(message, namecaraction):
    newtyres = message.text
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Cars (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, OwnerId INTEGER NOT NULL, Auto TEXT NOT NULL, RegPlate TEXT NOT NULL, Tyres TEXT NOT NULL, HP INTEGER NOT NULL, Weight INTEGER NOT NULL, EngineType TEXT NOT NULL, DriveUnit TEXT NOT NULL , TransmissionType TEXT NOT NULL)")
        cursor.execute("UPDATE Cars SET Tyres='{}' WHERE Auto='{}' AND OwnerId={}".format(newtyres, namecaraction, message.chat.id))
        conn.commit()
    bot.send_message(message.from_user.id, 'Название резины было изменено на: *{}*'.format(newtyres), parse_mode="Markdown")
    get_car_user(message)


def change_hp_car(message, namecaraction):
    newhp = message.text
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Cars (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, OwnerId INTEGER NOT NULL, Auto TEXT NOT NULL, RegPlate TEXT NOT NULL, Tyres TEXT NOT NULL, HP INTEGER NOT NULL, Weight INTEGER NOT NULL, EngineType TEXT NOT NULL, DriveUnit TEXT NOT NULL , TransmissionType TEXT NOT NULL)")
        cursor.execute("UPDATE Cars SET HP={} WHERE Auto='{}' AND OwnerId={}".format(newhp, namecaraction, message.chat.id))
        conn.commit()
    bot.send_message(message.from_user.id, 'Количество лошадиных сил было изменено на: *{}*'.format(newhp), parse_mode="Markdown")
    get_car_user(message)

def change_weight_car(message, namecaraction):
    newweight = message.text
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Cars (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, OwnerId INTEGER NOT NULL, Auto TEXT NOT NULL, RegPlate TEXT NOT NULL, Tyres TEXT NOT NULL, HP INTEGER NOT NULL, Weight INTEGER NOT NULL, EngineType TEXT NOT NULL, DriveUnit TEXT NOT NULL , TransmissionType TEXT NOT NULL)")
        cursor.execute("UPDATE Cars SET Weight={} WHERE Auto='{}' AND OwnerId={}".format(newweight, namecaraction, message.chat.id))
        conn.commit()
    bot.send_message(message.from_user.id, 'Вес авто был изменён на: *{}*'.format(newweight), parse_mode="Markdown")
    get_car_user(message)

def change_engine_car(message, namecaraction):
    newengine = message.text
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Cars (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, OwnerId INTEGER NOT NULL, Auto TEXT NOT NULL, RegPlate TEXT NOT NULL, Tyres TEXT NOT NULL, HP INTEGER NOT NULL, Weight INTEGER NOT NULL, EngineType TEXT NOT NULL, DriveUnit TEXT NOT NULL , TransmissionType TEXT NOT NULL)")
        cursor.execute("UPDATE Cars SET EngineType='{}' WHERE Auto='{}' AND OwnerId={}".format(newengine, namecaraction, message.chat.id))
        conn.commit()
    bot.send_message(message.from_user.id, 'Тип привода был изменён на: *{}*'.format(newengine), parse_mode="Markdown")
    get_car_user(message)

def change_drive_car(message, namecaraction):
    newdriveunit = message.text
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Cars (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, OwnerId INTEGER NOT NULL, Auto TEXT NOT NULL, RegPlate TEXT NOT NULL, Tyres TEXT NOT NULL, HP INTEGER NOT NULL, Weight INTEGER NOT NULL, EngineType TEXT NOT NULL, DriveUnit TEXT NOT NULL , TransmissionType TEXT NOT NULL)")
        cursor.execute("UPDATE Cars SET DriveUnit='{}' WHERE Auto='{}' AND OwnerId={}".format(newdriveunit, namecaraction, message.chat.id))
        conn.commit()
    bot.send_message(message.from_user.id, 'Тип двигателя был изменён на: *{}*'.format(newdriveunit), parse_mode="Markdown")
    get_car_user(message)

def change_trans_car(message, namecaraction):
    newtrans = message.text
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Cars (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, OwnerId INTEGER NOT NULL, Auto TEXT NOT NULL, RegPlate TEXT NOT NULL, Tyres TEXT NOT NULL, HP INTEGER NOT NULL, Weight INTEGER NOT NULL, EngineType TEXT NOT NULL, DriveUnit TEXT NOT NULL , TransmissionType TEXT NOT NULL)")
        cursor.execute("UPDATE Cars SET TransmissionType='{}' WHERE Auto='{}' AND OwnerId={}".format(newtrans, namecaraction, message.chat.id))
        conn.commit()
    bot.send_message(message.from_user.id, 'Тип трансмиссии был изменён на: *{}*'.format(newtrans), parse_mode="Markdown")
    get_car_user(message)


def get_name(message):
    datatime = now.strftime("%d-%m-%Y %H:%M")
    chatid = message.from_user.id
    name = message.text
    bot.send_message(message.from_user.id, 'Введите вашу фамилию: ')
    bot.register_next_step_handler(message, get_surname, datatime, chatid, name)

def get_surname(message, datatime, chatid, name):
    surname = message.text
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(message.from_user.id, 'Введите ваш номер телефона: ', reply_markup=keyboard)
    bot.register_next_step_handler(message, get_mobile_phone, datatime, chatid, name, surname)

def get_mobile_phone(message, datatime, chatid, name, surname):
    if message.contact is not None:
        mobilephone = message.contact.phone_number
    else:
        mobilephone = '380000000000'
    insert_sql_new(chatid, name, surname, mobilephone, datatime)
    keyboard = types.ReplyKeyboardRemove()
    admins_send(chatid, name, surname, mobilephone, datatime)
    try:
        bot.send_message(message.from_user.id, "Регистрация завершена, ожидайте одобрения вашей заявки администратором.", reply_markup=keyboard)
    except:
        pass

######### the end register

def get_car_name(message, ownerid):
    auto = message.text
    bot.send_message(message.from_user.id, 'Введите автомобильный номер: ')
    bot.register_next_step_handler(message, get_car_regplate, ownerid, auto)

def get_car_regplate(message, ownerid, auto):
    regplate = message.text
    bot.send_message(message.from_user.id, 'Введите название шин: ')
    bot.register_next_step_handler(message, get_car_tyres, ownerid, auto, regplate)

def get_car_tyres(message, ownerid, auto, regplate):
    tyres = message.text
    bot.send_message(message.from_user.id, 'Введите количество лошадиных сил двигателя: ')
    bot.register_next_step_handler(message, get_car_hp, ownerid, auto, regplate, tyres)

def get_car_hp(message, ownerid, auto, regplate, tyres):
    hp = message.text
    bot.send_message(message.from_user.id, 'Введите вес авто в килогараммах: ')
    bot.register_next_step_handler(message, get_car_weight, ownerid, auto, regplate, tyres, hp)

def get_car_weight(message, ownerid, auto, regplate, tyres, hp):
    weight = message.text
    tranv = telebot.types.ReplyKeyboardMarkup(True, True)
    tranv.row('Бензиновый')
    tranv.row('Дизельный')
    tranv.row('Электро')
    bot.send_message(message.from_user.id, 'Выберите тип двигателя: ', reply_markup=tranv)
    bot.register_next_step_handler(message, get_car_unit, ownerid, auto, regplate, tyres, hp, weight)

def get_car_unit(message, ownerid, auto, regplate, tyres, hp, weight):
    drive_unit = message.text
    tranv = telebot.types.ReplyKeyboardMarkup(True, True)
    tranv.row('Полный')
    tranv.row('Передний')
    tranv.row('Задний')
    bot.send_message(message.from_user.id, 'Выберите тип привода: ', reply_markup=tranv)
    bot.register_next_step_handler(message, get_car_engine, ownerid, auto, regplate, tyres, hp, weight, drive_unit)


def get_car_engine(message, ownerid, auto, regplate, tyres, hp, weight, drive_unit):
    engine = message.text
    #
    tranv = telebot.types.ReplyKeyboardMarkup(True, True)
    tranv.row('Автомат')
    tranv.row('Механика')
    tranv.row('Робот')
    #
    bot.send_message(message.from_user.id, 'Укажите вид трансмиссии: ', reply_markup=tranv)
    bot.register_next_step_handler(message, get_car_trans, ownerid, auto, regplate, tyres, hp, weight, drive_unit, engine)

def get_car_trans(message, ownerid, auto, regplate, tyres, hp, weight, drive_unit, engine):
    trans = message.text

    ##
    check = check_reg(message.from_user.id)
    ##
    try:
        insert_sql_car(ownerid, auto, regplate, tyres, hp, weight, drive_unit, engine, trans)
        if check == 3:
            bot.send_message(message.from_user.id, 'Автомобиль «{}» успешно добавлен в ваш гараж.'.format(auto), reply_markup=default_menu_user())
        elif check == 4:
            bot.send_message(message.from_user.id, 'Автомобиль «{}» успешно добавлен в ваш гараж.'.format(auto), reply_markup=default_menu_admin())
    except:
        if check == 3:
            bot.send_message(message.from_user.id, '[Ошибка] Автомобиль не был добавлен в гараж, попробуйте снова.', reply_markup=default_menu_user())
        elif check == 4:
            bot.send_message(message.from_user.id, '[Ошибка] Автомобиль не был добавлен в гараж, попробуйте снова.', reply_markup=default_menu_admin())


######## блок общения добавления тачки







def insert_sql_new(chatid, name, surname, mobilephone, datatime):
    try:
        with sqlite3.connect("static/database/main.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Users (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, FirstName TEXT NOT NULL, LastName TEXT NOT NULL, TGUserId INTEGER NOT NULL, MobilePhone NUMERIC NOT NULL, DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Status INTEGER NOT NULL DEFAULT 2, Alerts INTEGER NOT NULL DEFAULT 0)")
            cursor.execute("INSERT INTO Users (FirstName, LastName, TGUserId, MobilePhone, DateCreated, Status, Alerts) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(name, surname, chatid, mobilephone, datatime, 2, 0))
            conn.commit()
    except:
        pass

def insert_sql_car(ownerid, auto, regplate, tyres, hp, weight, drive_unit, engine, trans):
    try:
        with sqlite3.connect("static/database/main.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Cars (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, OwnerId INTEGER NOT NULL, Auto TEXT NOT NULL, RegPlate TEXT NOT NULL, Tyres TEXT NOT NULL, HP INTEGER NOT NULL, Weight INTEGER NOT NULL, EngineType TEXT NOT NULL, DriveUnit TEXT NOT NULL , TransmissionType TEXT NOT NULL)")
            cursor.execute("INSERT INTO Cars (OwnerId, Auto, RegPlate, Tyres, HP, Weight, EngineType, DriveUnit, TransmissionType) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(ownerid, auto, regplate, tyres, hp, weight, engine, drive_unit, trans))
            conn.commit()
    except:
        pass



def admins_send(chatid, name, surname, mobilephone, datatime):
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE Status=4")
        result = cursor.fetchall()
        conn.commit()

    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="Одобрить", callback_data="1")
    but_2 = types.InlineKeyboardButton(text="Отклонить", callback_data="2")
    key.add(but_1, but_2)

    for num in result:
        try:
            bot.send_message(num[3], "[Запрос регистрации]\n TelegramChatID: {} \n Имя: {} \n Фамилия: {} \n Мобильный: {} \n Дата регистрации: {}".format(chatid, name, surname, mobilephone, datatime), reply_markup=key)
        except:
            pass


def default_menu_admin():
    carbut = telebot.types.ReplyKeyboardMarkup(True, True)
    carbut.row('Панель администратора')
    carbut.row('Регистрация на мероприятие')
    carbut.row('Мои автомобили')
    carbut.row('Мой ТОП-10')
    carbut.row('Общий ТОП-10')
    carbut.row('Настройки')
    return carbut

def default_menu_user():
    carbut = telebot.types.ReplyKeyboardMarkup(True, True)
    carbut.row('Регистрация на мероприятие')
    carbut.row('Мои автомобили')
    carbut.row('Мой ТОП-10')
    carbut.row('Общий ТОП-10')
    carbut.row('Настройки')
    return carbut

def default_menu_admin_action():
    carbut = telebot.types.ReplyKeyboardMarkup(True, True)
    carbut.row('Управление мероприятиями')
    carbut.row('Cписок запросов на регистрацию')
    carbut.row('<< Назад')
    return carbut

def default_start_button():
    carbut = telebot.types.ReplyKeyboardMarkup(True, True)
    carbut.row('/start')
    return carbut

def default_mp_action():
    carbut = telebot.types.ReplyKeyboardMarkup(True, True)
    carbut.row('Список мероприятий')
    carbut.row('Добавить мероприятие')
    carbut.row('<< Назад')
    return carbut


def testov(message):
    result = get_usr()
    key = types.InlineKeyboardMarkup()
    but_1 = types.InlineKeyboardButton(text="Одобрить", callback_data="1")
    but_2 = types.InlineKeyboardButton(text="Отклонить", callback_data="2")
    key.add(but_1, but_2)
    for num in result:
        bot.send_message(message.chat.id, text="[Запрос регистрации]\n TelegramChatID: {} \n Имя: {} \n Фамилия: {} \n Мобильный: {} \n Дата регистрации: {}".format(num[3], num[1], num[2], num[4], num[5]), reply_markup=key)
    bot.send_message(message.chat.id, "Вы находитесь в панели администратора.", reply_markup=default_menu_admin_action())
    bot.register_next_step_handler(message, admin_panel)


def get_usr():
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Users (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, FirstName TEXT NOT NULL, LastName TEXT NOT NULL, TGUserId INTEGER NOT NULL, MobilePhone NUMERIC NOT NULL, DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Status INTEGER NOT NULL DEFAULT 2, Alerts INTEGER NOT NULL DEFAULT 0)")
        cursor.execute("SELECT * FROM Users WHERE Status=2")
        result = cursor.fetchall()
        conn.commit()
    return result



@bot.callback_query_handler(func=lambda call_b:True) ##### inline accept register user
def inlin(call_b):
    x = call_b.message.text.split(" ")
    if call_b.data == '1':
        with sqlite3.connect("static/database/main.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS MP_Result (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpId INTEGER NOT NULL, MpUserId INTEGER NOT NULL, Result FLOAT NOT NULL, UserCar TEXT NOT NULL, UStatus INTEGER NOT NULL)")
            cursor.execute("SELECT Status FROM Users WHERE TGUserId={}".format(x[3]))
            user_status = cursor.fetchone()
            conn.commit()
        ####
        if user_status == None or user_status[0] == 1:
            bot.delete_message(call_b.message.chat.id, call_b.message.message_id)
            bot.send_message(call_b.message.chat.id, "*(Х)* Данная заявка уже *обработана* и *отклонена* другим администратором.", parse_mode="Markdown", reply_markup=default_menu_admin())
        elif user_status[0] == 3 or user_status[0] == 4:
            bot.delete_message(call_b.message.chat.id, call_b.message.message_id)
            bot.send_message(call_b.message.chat.id, "*(Х)* Данная заявка уже *обработана* и *одобрена* другим администратором.", parse_mode="Markdown", reply_markup=default_menu_admin())
        elif user_status[0] == 2:
        ######
            bot.delete_message(call_b.message.chat.id, call_b.message.message_id)
            bot.send_message(call_b.message.chat.id, "(ACCEPT) Заявка пользователя *{} {}* \n(TGuId: {}) на регистрацию была *ОДОБРЕНА*.".format(x[6], x[9],  x[3]), parse_mode="Markdown")
            try:
                update_sql_reg(1, x)
            except:
                pass

            try:
                bot.send_message(x[3], "Здравствуйте, ваша заявка на регистрацию *одобрена* администратором.", parse_mode="Markdown")
            except:
                pass
    elif call_b.data == '2':

        with sqlite3.connect("static/database/main.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS MP_Result (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpId INTEGER NOT NULL, MpUserId INTEGER NOT NULL, Result FLOAT NOT NULL, UserCar TEXT NOT NULL, UStatus INTEGER NOT NULL)")
            cursor.execute("SELECT Status FROM Users WHERE TGUserId={}".format(x[3]))
            user_status = cursor.fetchone()
            conn.commit()
        ####
        if user_status == None or user_status[0] == 1:
            bot.delete_message(call_b.message.chat.id, call_b.message.message_id)
            bot.send_message(call_b.message.chat.id, "*(Х)* Данная заявка уже *обработана* и *отклонена* другим администратором.", parse_mode="Markdown", reply_markup=default_menu_admin())
        elif user_status[0] == 3 or user_status[0] == 4:
            bot.delete_message(call_b.message.chat.id, call_b.message.message_id)
            bot.send_message(call_b.message.chat.id, "*(Х)* Данная заявка уже *обработана* и *одобрена* другим администратором.", parse_mode="Markdown", reply_markup=default_menu_admin())
        elif user_status[0] == 2:
            bot.delete_message(call_b.message.chat.id, call_b.message.message_id)
            bot.send_message(call_b.message.chat.id, "(NOT ACCEPT) Заявка пользователя *{} {}* \n(TGuId: {}) на регистрацию была *ОТКЛОНЕНА*.".format(x[6], x[9],  x[3]), parse_mode="Markdown")
            try:
                update_sql_reg(2, x)
            except:
                pass

            try:
                bot.send_message(x[3], "Здравствуйте, ваша заявка на регистрацию *отклонена* администратором.", parse_mode="Markdown")
            except:
                pass

    elif call_b.data == '3':
        with sqlite3.connect("static/database/main.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS MP_Result (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpId INTEGER NOT NULL, MpUserId INTEGER NOT NULL, Result FLOAT NOT NULL, UserCar TEXT NOT NULL, UStatus INTEGER NOT NULL)")
            cursor.execute("SELECT UStatus FROM MP_Result WHERE (MpId={}) AND (MpUserId={})".format(x[14], x[5]))
            user_status = cursor.fetchone()
            conn.commit()
        ####
        if user_status == None:
            bot.delete_message(call_b.message.chat.id, call_b.message.message_id)
            bot.send_message(call_b.message.chat.id, "*(Х)* Данная заявка уже *обработана* и *отклонена* другим администратором.", parse_mode="Markdown", reply_markup=default_menu_admin())
        elif user_status[0] == 1:
            bot.delete_message(call_b.message.chat.id, call_b.message.message_id)
            bot.send_message(call_b.message.chat.id, "*(Х)* Данная заявка уже *обработана* и *одобрена* другим администратором.", parse_mode="Markdown", reply_markup=default_menu_admin())
        elif user_status[0] == 0:
            ######
            with sqlite3.connect("static/database/main.sqlite") as conn:
                cursor = conn.cursor()
                cursor.execute("CREATE TABLE IF NOT EXISTS MP (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpName TEXT NOT NULL, MpDate TEXT NOT NULL, MpTime TEXT NOT NULL, MpWeather TEXT NOT NULL, MpTemp INTEGER NOT NULL, MpMember INTEGER NOT NULL, MpMemberMax INTEGER NOT NULL, Status INTEGER NOT NULL)")
                cursor.execute("SELECT MpMember, MpMemberMax FROM MP WHERE Id={}".format(x[14]))
                result = cursor.fetchone()
                conn.commit()
            if result[1] < result[0]:
                bot.delete_message(call_b.message.chat.id, call_b.message.message_id)
                bot.send_message(call_b.message.chat.id,"(ACCEPT) Заявка пользователя *{} {}* \n(TGuId: {}) на гонку была *ОДОБРЕНА*.".format(x[8], x[11], x[5]), parse_mode="Markdown")
                #######
                try:
                    with sqlite3.connect("static/database/main.sqlite") as conn:
                        cursor = conn.cursor()
                        cursor.execute("CREATE TABLE IF NOT EXISTS MP_Result (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpId INTEGER NOT NULL, MpUserId INTEGER NOT NULL, Result FLOAT NOT NULL, UserCar TEXT NOT NULL, UStatus INTEGER NOT NULL)")
                        cursor.execute("UPDATE MP_Result SET UStatus=1 WHERE (MpId={}) AND (MpUserId={})".format(x[14], x[5]))
                        #
                        cursor.execute("CREATE TABLE IF NOT EXISTS MP (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpName TEXT NOT NULL, MpDate TEXT NOT NULL, MpTime TEXT NOT NULL, MpWeather TEXT NOT NULL, MpTemp INTEGER NOT NULL, MpMember INTEGER NOT NULL, MpMemberMax INTEGER NOT NULL, Status INTEGER NOT NULL)")
                        mmax = int(result[1]) + 1
                        cursor.execute("Update MP SET MpMemberMax={} WHERE Id={}".format(mmax, x[14]))
                        conn.commit()
                except:
                    pass
                ########
                try:
                    bot.send_message(x[5], "Здравствуйте, ваша заявка регистрации на гонку: \n*№{} {}*Время проведения: *{} {}*\n*одобрена* администратором.".format(x[14], x[16], x[19], x[23]), parse_mode="Markdown")
                except:
                    pass
            else:
                # если все места заняты
                bot.delete_message(call_b.message.chat.id, call_b.message.message_id)
                bot.send_message(call_b.message.chat.id,"(NOT ACCEPT) Заявка пользователя *{} {}* \n(TGuId: {}) на гонку была *ОТКЛОНЕНА*.\nПричина: *Нет мест*".format(x[8],x[11],x[5]), parse_mode="Markdown")
                ####
                with sqlite3.connect("static/database/main.sqlite") as conn:
                    cursor = conn.cursor()
                    cursor.execute("CREATE TABLE IF NOT EXISTS MP_Result (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpId INTEGER NOT NULL, MpUserId INTEGER NOT NULL, Result FLOAT NOT NULL, UserCar TEXT NOT NULL, UStatus INTEGER NOT NULL)")
                    cursor.execute("SELECT * FROM MP_Result WHERE (UStatus=0) AND MpId={}".format(x[14]))
                    kick = cursor.fetchall()
                    cursor.execute("DELETE FROM MP_Result WHERE (UStatus=0) AND MpId={}".format(x[14]))
                    conn.commit()
                for nim in kick:
                    try:
                        bot.send_message(nim[2], "Здравствуйте, к сожалению все места на гонку: \n*№{} {}*Время проведения: *{} {}*\n*закончились*, регистрируйтесь на другую.".format(x[14], x[16], x[19], x[23]), parse_mode="Markdown")
                    except:
                        pass
                #####

    elif call_b.data == '4':
        ####
        with sqlite3.connect("static/database/main.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS MP_Result (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpId INTEGER NOT NULL, MpUserId INTEGER NOT NULL, Result FLOAT NOT NULL, UserCar TEXT NOT NULL, UStatus INTEGER NOT NULL)")
            cursor.execute("SELECT UStatus FROM MP_Result WHERE (MpId={}) AND (MpUserId={})".format(x[14], x[5]))
            user_status = cursor.fetchone()
            conn.commit()
        ####
        if user_status == None:
            bot.delete_message(call_b.message.chat.id, call_b.message.message_id)
            bot.send_message(call_b.message.chat.id, "*(Х)* Данная заявка уже *обработана* и *отклонена* другим администратором.", parse_mode="Markdown", reply_markup=default_menu_admin())
        elif user_status[0] == 1:
            bot.delete_message(call_b.message.chat.id, call_b.message.message_id)
            bot.send_message(call_b.message.chat.id, "*(Х)* Данная заявка уже *обработана* и *одобрена* другим администратором.", parse_mode="Markdown", reply_markup=default_menu_admin())
        elif user_status[0] == 0:
            bot.delete_message(call_b.message.chat.id, call_b.message.message_id)
            bot.send_message(call_b.message.chat.id, "(NOT ACCEPT) Заявка пользователя *{} {}* \n(TGuId: {}) на гонку была *ОТКЛОНЕНА*.".format(x[8], x[11], x[5]), parse_mode="Markdown")
            try:
                ##
                with sqlite3.connect("static/database/main.sqlite") as conn:
                    cursor = conn.cursor()
                    cursor.execute("CREATE TABLE IF NOT EXISTS MP_Result (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpId INTEGER NOT NULL, MpUserId INTEGER NOT NULL, Result FLOAT NOT NULL, UserCar TEXT NOT NULL, UStatus INTEGER NOT NULL)")
                    cursor.execute("DELETE FROM MP_Result WHERE (MpId={}) AND (MpUserId={})".format(x[14],x[5]))
                    conn.commit()
                ##
            except:
                pass

            try:
                bot.send_message(x[5], "Здравствуйте, ваша заявка регистрации на гонку: \n*№{} {}*Время проведения: *{} {}*\n*отклонена* администратором.".format(x[14], x[16], x[19], x[23]),parse_mode="Markdown")
            except:
                pass

def update_sql_reg(y, x):
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Users (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, FirstName TEXT NOT NULL, LastName TEXT NOT NULL, TGUserId INTEGER NOT NULL, MobilePhone NUMERIC NOT NULL, DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Status INTEGER NOT NULL DEFAULT 2, Alerts INTEGER NOT NULL DEFAULT 0)")
        if y == 1:
            cursor.execute("UPDATE Users SET Status=3 WHERE TGUserId={}".format(x[3]))
        elif y == 2:
            cursor.execute("UPDATE Users SET Status=1 WHERE TGUserId={}".format(x[3]))
        conn.commit()


if __name__ == '__main__':
    bot.polling(none_stop=True, timeout=100)