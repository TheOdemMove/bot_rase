import telebot
from telebot import types
import datetime
import sqlite3
import telebot_calendar
from telebot_calendar import CallbackData
from telebot.types import ReplyKeyboardRemove, CallbackQuery



bot = telebot.TeleBot('1452247200:AAES4nlaN4zg6-J6ljkDssrcfJYpBVdw3sU')
now = datetime.datetime.now()
calendar_1 = CallbackData("calendar_1", "action", "year", "month", "day")
ccalendar = False


@bot.message_handler(commands=['start'])
def phone(message):
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




def check_reg(id):
    try:
        with sqlite3.connect("static/database/main.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Cars (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, OwnerId INTEGER NOT NULL, Auto TEXT NOT NULL, RegPlate TEXT NOT NULL, Tyres TEXT NOT NULL, HP INTEGER NOT NULL, Weight INTEGER NOT NULL, EngineType TEXT NOT NULL, DriveUnit TEXT NOT NULL , TransmissionType TEXT NOT NULL)")
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
    global ownerid
    check = check_reg(message.from_user.id)
    if check == 1:
        if message.text == 'Регистрация':
            ###
            print(check)
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
        else:
            bot.send_message(message.from_user.id, 'Простите, я не понимаю вас, используйте команду - /start', reply_markup=default_start_button())
    elif check == 4:
        if message.text == 'Панель администратора':
            bot.send_message(message.from_user.id, "Используйте меню, для выбора действий.", reply_markup=default_menu_admin_action())
            bot.register_next_step_handler(message, admin_panel)
        elif message.text == 'Мои автомобили':
            get_car_user(message)
        else:
            bot.send_message(message.from_user.id, 'Простите, я не понимаю вас, используйте команду - /start', reply_markup=default_start_button())

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
            cursor.execute("CREATE TABLE IF NOT EXISTS MP (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpName TEXT NOT NULL, MpDate TEXT NOT NULL, MpTime TEXT NOT NULL, MpWeather TEXT NOT NULL, MpTemp INTEGER NOT NULL, MpMember INTEGER NOT NULL)")
            cursor.execute("SELECT * FROM MP")
            result = cursor.fetchall()
            conn.commit()
        if len(result) > 0:
            mpbut = telebot.types.ReplyKeyboardMarkup(True, True)
            for num in result:
                mpbut.row('ID: {} | Name: {}\nDate: {} | Time: {}'.format(num[0], num[1], num[2], num[3]))
            mpbut.row('<< Назад')
            bot.send_message(message.from_user.id, "Здесь отображены крайние 10 мероприятий, для добавления результатов гонок выберите мероприятие.", reply_markup=mpbut)
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
        bot.send_message(message.from_user.id, 'Окей, ты выбрал вот это: \n{}'.format(message.text), reply_markup=default_mp_action())
    bot.register_next_step_handler(message, menu_mp)

def add_mp(message):
    global mp_name
    mp_name = message.text
    bot.send_message(message.from_user.id, "Укажите дату проведения\n(пример 29.01.2021): ")
    bot.register_next_step_handler(message, add_mp_date)

def add_mp_date(message):
    global mp_date
    mp_date = message.text
    bot.send_message(message.from_user.id, "Укажите время проведения\n(например - 15:00): ")
    bot.register_next_step_handler(message, add_mp_time)

def add_mp_time(message):
    global mp_time
    mp_time = message.text
    bot.send_message(message.from_user.id, "Укажите погодные условия: ")
    bot.register_next_step_handler(message, add_mp_weather)

def add_mp_weather(message):
    global mp_weather
    mp_weather = message.text
    bot.send_message(message.from_user.id, "Укажите температуру воздуха: ")
    bot.register_next_step_handler(message, add_mp_temp)

def add_mp_temp(message):
    global mp_temp
    mp_temp = message.text
    bot.send_message(message.from_user.id, "Укажите количество участников: ")
    bot.register_next_step_handler(message, add_mp_member)

def add_mp_member(message):
    global mp_member
    mp_member = message.text
    insert_sql_mp(message)

def insert_sql_mp(message):
    create_mp = "Мероприятие *'{}'*\nуспешно создано.\n*Дата проведения:* {}\n*Время проведения:* {}\n*Погода:* {}\n*Температура:* {}\n*Макс. кол-во участников:* {}\n".format(mp_name, mp_date, mp_time, mp_weather, mp_temp, mp_member)
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS MP (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, MpName TEXT NOT NULL, MpDate TEXT NOT NULL, MpTime TEXT NOT NULL, MpWeather TEXT NOT NULL, MpTemp INTEGER NOT NULL, MpMember INTEGER NOT NULL)")
        cursor.execute("INSERT INTO MP (MpName, MpDate, MpTime, MpWeather, MpTemp, MpMember) values ('{}', '{}', '{}', '{}', '{}', '{}')".format(mp_name, mp_date, mp_time, mp_weather, mp_temp, mp_member))
        conn.commit()
    bot.send_message(message.from_user.id, create_mp, parse_mode="Markdown", reply_markup=default_mp_action())
    bot.register_next_step_handler(message, menu_mp)


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
            bot.register_next_step_handler(message, next_hop)
        elif check == 4:
            bot.send_message(message.from_user.id, "В вашем гараже еще нет автомобилей. \nВоспользуйтесь кнопкой: \n*'Добавить автомобиль'*.", parse_mode="Markdown", reply_markup=mycar)
            bot.register_next_step_handler(message, next_hop)
    else:
        bot.send_message(message.from_user.id, "В вашем гараже сейчас {} автомобиля(ей), для управления выберите автомобиль. \n\nЕсли хотите добавить новый, используйте кнопку: \n*'Добавить автомобиль'*".format(str(count)), parse_mode="Markdown", reply_markup=mycar)
        bot.register_next_step_handler(message, next_car_action)


def next_hop(message):
    carbut = types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, "Что бы добавить автомобиль в гараж, следуйте дальнейшим инструкциям бота.", reply_markup=carbut)
    global ownerid
    ownerid = message.from_user.id
    bot.send_message(message.from_user.id, "Введите название марки авто: ")
    bot.register_next_step_handler(message, get_car_name)


def next_car_action(message):
    namecaraction = message.text
    check = check_reg(message.from_user.id)
    if check == 3:
        if message.text == "Добавить автомобиль":
            next_hop(message)
        elif message.text == "<< Назад":
            bot.send_message(message.from_user.id, "Вы вернулись в главное меню.", reply_markup=default_menu_user())
        else:
            bot.send_message(message.from_user.id, "Car choise: {}".format(namecaraction), reply_markup=default_menu_user())
    elif check == 4:
        if message.text == "Добавить автомобиль":
            next_hop(message)
        elif message.text == "<< Назад":
            bot.send_message(message.from_user.id, "Вы вернулись в главное меню.", reply_markup=default_menu_admin())
        else:
            bot.send_message(message.from_user.id, "Car choise: {}".format(namecaraction), reply_markup=default_menu_admin())



### блок общения для регистрации
#####
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
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(message.from_user.id, 'Введите ваш номер телефона: ', reply_markup=keyboard)
    bot.register_next_step_handler(message, get_mobile_phone)

def get_mobile_phone(message):
    global mobilephone
    if message.contact is not None:
        mobilephone = message.contact.phone_number
    else:
        mobilephone = '380000000000'
    insert_sql_new()
    keyboard = types.ReplyKeyboardRemove()
    admins_send()
    try:
        bot.send_message(message.from_user.id, "Регистрация завершена, ожидайте одобрения вашей заявки администратором.", reply_markup=keyboard)
    except:
        pass

######### the end register

def get_car_name(message):
    global auto
    auto = message.text
    bot.send_message(message.from_user.id, 'Введите автомобильный номер: ')
    bot.register_next_step_handler(message, get_car_regplate)

def get_car_regplate(message):
    global regplate
    regplate = message.text
    bot.send_message(message.from_user.id, 'Введите тип шин: ')
    bot.register_next_step_handler(message, get_car_tyres)

def get_car_tyres(message):
    global tyres
    tyres = message.text
    bot.send_message(message.from_user.id, 'Введите количество лошадиных сил двигателя: ')
    bot.register_next_step_handler(message, get_car_hp)

def get_car_hp(message):
    global hp
    hp = message.text
    bot.send_message(message.from_user.id, 'Введите вес авто в килогараммах: ')
    bot.register_next_step_handler(message, get_car_weight)

def get_car_weight(message):
    global weight
    weight = message.text
    tranv = telebot.types.ReplyKeyboardMarkup(True, True)
    tranv.row('Бензиновый')
    tranv.row('Дизельный')
    tranv.row('Электро')
    bot.send_message(message.from_user.id, 'Выберите тип двигателя: ', reply_markup=tranv)
    bot.register_next_step_handler(message, get_car_unit)

def get_car_unit(message):
    global drive_unit
    drive_unit = message.text
    tranv = telebot.types.ReplyKeyboardMarkup(True, True)
    tranv.row('Полный')
    tranv.row('Передний')
    tranv.row('Задний')
    bot.send_message(message.from_user.id, 'Выберите тип привода: ', reply_markup=tranv)
    bot.register_next_step_handler(message, get_car_engine)


def get_car_engine(message):
    global engine
    engine = message.text
    #
    tranv = telebot.types.ReplyKeyboardMarkup(True, True)
    tranv.row('Автомат')
    tranv.row('Механика')
    tranv.row('Робот')
    #
    bot.send_message(message.from_user.id, 'Укажите вид трансмиссии: ', reply_markup=tranv)
    bot.register_next_step_handler(message, get_car_trans)

def get_car_trans(message):
    global trans
    trans = message.text

    ##
    check = check_reg(message.from_user.id)
    ##
    try:
        insert_sql_car()
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







def insert_sql_new():
    try:
        with sqlite3.connect("static/database/main.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Users (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, FirstName TEXT NOT NULL, LastName TEXT NOT NULL, TGUserId INTEGER NOT NULL, MobilePhone NUMERIC NOT NULL, DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Status INTEGER NOT NULL DEFAULT 2)")
            cursor.execute("INSERT INTO Users (FirstName, LastName, TGUserId, MobilePhone, DateCreated, Status) values ('{}', '{}', '{}', '{}', '{}', '{}')".format(name, surname, chatid, mobilephone, datatime, 2))
            conn.commit()
    except:
        pass

def insert_sql_car():
    try:
        with sqlite3.connect("static/database/main.sqlite") as conn:
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS Cars (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, OwnerId INTEGER NOT NULL, Auto TEXT NOT NULL, RegPlate TEXT NOT NULL, Tyres TEXT NOT NULL, HP INTEGER NOT NULL, Weight INTEGER NOT NULL, EngineType TEXT NOT NULL, DriveUnit TEXT NOT NULL , TransmissionType TEXT NOT NULL)")
            cursor.execute("INSERT INTO Cars (OwnerId, Auto, RegPlate, Tyres, HP, Weight, EngineType, DriveUnit, TransmissionType) values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(ownerid, auto, regplate, tyres, hp, weight, engine, drive_unit, trans))
            conn.commit()
    except:
        pass



def admins_send():
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE Status=4")
        result = cursor.fetchall()
        conn.commit()
    for num in result:
        try:
            bot.send_message(num[3], "[Запрос регистрации]\nTelegramChatID: {}\nИмя: {}\nФамилия: {}\nМобильный: {}\nДата регистрации: {}".format(chatid, name, surname, mobilephone, datatime))
        except:
            pass


def default_menu_admin():
    carbut = telebot.types.ReplyKeyboardMarkup(True, True)
    carbut.row('Панель администратора')
    carbut.row('Мои автомобили')
    carbut.row('Мой ТОП-10')
    carbut.row('Общий ТОП-10')
    return carbut

def default_menu_user():
    carbut = telebot.types.ReplyKeyboardMarkup(True, True)
    carbut.row('Мои автомобили')
    carbut.row('Мой ТОП-10')
    carbut.row('Общий ТОП-10')
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
    for num in result:
        bot.send_message(message.chat.id, text="[Запрос регистрации]\nTGUserId: {}\nИмя, Фамилия: {} {}\nТелефон: {}\nДата регистрации: {}\n\n".format(num[3], num[1], num[2], num[4], num[5]), reply_markup=default_menu_admin_action())
    bot.register_next_step_handler(message, admin_panel)


def get_usr():
    with sqlite3.connect("static/database/main.sqlite") as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS Users (Id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE, FirstName TEXT NOT NULL, LastName TEXT NOT NULL, TGUserId INTEGER NOT NULL, MobilePhone NUMERIC NOT NULL, DateCreated TIMESTAMP DEFAULT CURRENT_TIMESTAMP, Status INTEGER NOT NULL DEFAULT 2)")
        cursor.execute("SELECT * FROM Users WHERE Status=2")
        result = cursor.fetchall()
        conn.commit()
    return result



# @bot.callback_query_handler(func=lambda call: True)
# def query_handler(call):
#     bot.answer_callback_query(callback_query_id=call.id, text='Права пользователя были изменены.')
#     answer = ''
#     if call.data == '10':
#         answer = 'Регистрация пользователя была одобрена.'
#     elif call.data == '11':
#         answer = 'Регистрация пользователя была отклонена.'
#     bot.send_message(call.message.chat.id, answer)


bot.polling(none_stop=True, timeout=500)