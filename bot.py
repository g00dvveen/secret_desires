import config
import telebot
from telebot import types


bot = telebot.TeleBot(config.token)
user_names = {
    '185542622': 'Фома',
    '858029609': 'Веня'
}
user_sex = {
    '185542622': 'male',
    '858029609': 'male'
}
user_age = {
    '185542622': '37',
    '858029609': '35'
}
user_nicknames = {
    'foma': '185542622',
    'ven': '858029609'
}
user_partners = {
}

# user_names = {}
# user_sex = {}
# user_age = {}
# user_nicknames = {}
# user_partners = {}


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = str(message.from_user.id)
    if user_id in user_names:
        bot.send_message(user_id, 'Привет, '+user_names[user_id])
        show_main_menu(user_id)
    else:
        sent = bot.send_message(user_id, 'Давай знакомиться! Как тебя зовут?')
        bot.register_next_step_handler(sent, lambda m: acquaint(m, user_id))


@bot.message_handler(commands=['help'])
def start_message(message):
    user_id = str(message.from_user.id)
    show_help(user_id)


def acquaint(message, user_id):
    user_names[user_id] = message.text
    sex_keyboard = types.InlineKeyboardMarkup()
    key_male = types.InlineKeyboardButton(text='Мужской', callback_data='set_sex_male')
    sex_keyboard.add(key_male)
    key_female = types.InlineKeyboardButton(text='Женский', callback_data='set_sex_female')
    sex_keyboard.add(key_female)
    bot.send_message(user_id, text='Привет, '+user_names[user_id]+'!\nТвой пол', reply_markup=sex_keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    user_id = str(call.from_user.id)
    if call.data == "set_sex_male":
        user_sex[user_id] = 'male'
        sent = bot.send_message(user_id, 'Отлично! Сколько тебе лет?')
        bot.register_next_step_handler(sent, lambda m: set_age(m, user_id))
    elif call.data == "set_sex_female":
        user_sex[user_id] = 'female'
        sent = bot.send_message(user_id, 'Отлично! Сколько тебе лет?')
        bot.register_next_step_handler(sent, lambda m: set_age(m, user_id))
    elif call.data == "dinner":
        key_list = list(user_nicknames.keys())
        val_list = list(user_nicknames.values())
        position = (val_list.index(user_id))
        user_nickname = key_list[position]
        partner_nickname = user_partners[user_id]
        partner_user_id = user_nicknames[partner_nickname]
        bot.send_message(partner_user_id, 'Пользователь с ником '+user_nickname+' желает с тобой поужинать!')
        get_info_keyboard = types.InlineKeyboardMarkup()
        key_get_info = types.InlineKeyboardButton(text='Показать', callback_data='get_user_info,'+user_id)
        get_info_keyboard.add(key_get_info)
        bot.send_message(partner_user_id, 'Показать профиль', reply_markup=get_info_keyboard)
        bot.send_message(user_id, 'Пользователь с ником ' + partner_nickname + ' теперь знает о твоем желании.')
        show_main_menu(user_id)
    elif call.data == "cinema":
        key_list = list(user_nicknames.keys())
        val_list = list(user_nicknames.values())
        position = (val_list.index(user_id))
        user_nickname = key_list[position]
        partner_nickname = user_partners[user_id]
        partner_user_id = user_nicknames[partner_nickname]
        bot.send_message(partner_user_id, 'Пользователь с ником '+user_nickname+' желает сходить с тобой! в кино')
        get_info_keyboard = types.InlineKeyboardMarkup()
        key_get_info = types.InlineKeyboardButton(text='Показать', callback_data='get_user_info,'+user_id)
        get_info_keyboard.add(key_get_info)
        bot.send_message(partner_user_id, 'Показать профиль', reply_markup=get_info_keyboard)
        bot.send_message(user_id, 'Пользователь с ником ' + partner_nickname + ' теперь знает о твоем желании.')
        show_main_menu(user_id)
    elif call.data == "massage":
        key_list = list(user_nicknames.keys())
        val_list = list(user_nicknames.values())
        position = (val_list.index(user_id))
        user_nickname = key_list[position]
        partner_nickname = user_partners[user_id]
        partner_user_id = user_nicknames[partner_nickname]
        bot.send_message(partner_user_id, 'Пользователь с ником '+user_nickname+' желает получить от тебя массаж!')
        get_info_keyboard = types.InlineKeyboardMarkup()
        key_get_info = types.InlineKeyboardButton(text='Показать профиль', callback_data='get_user_info,'+user_id)
        key_send_message = types.InlineKeyboardButton(text='Отправить сообщение', callback_data='send_message,' + user_id)
        get_info_keyboard.add(key_get_info)
        get_info_keyboard.add(key_send_message)
        bot.send_message(partner_user_id, 'Интересно?', reply_markup=get_info_keyboard)
        bot.send_message(user_id, 'Пользователь с ником ' + partner_nickname + ' теперь знает о твоем желании.')
        show_main_menu(user_id)
    elif call.data == "sex":
        key_list = list(user_nicknames.keys())
        val_list = list(user_nicknames.values())
        position = (val_list.index(user_id))
        user_nickname = key_list[position]
        partner_nickname = user_partners[user_id]
        partner_user_id = user_nicknames[partner_nickname]
        bot.send_message(partner_user_id, 'Пользователь с ником '+user_nickname+' желает секса с тобой!')
        get_info_keyboard = types.InlineKeyboardMarkup()
        key_get_info = types.InlineKeyboardButton(text='Показать', callback_data='get_user_info,'+user_id)
        get_info_keyboard.add(key_get_info)
        bot.send_message(partner_user_id, 'Показать профиль', reply_markup=get_info_keyboard)
        bot.send_message(user_id, 'Пользователь с ником ' + partner_nickname + ' теперь знает о твоем желании.')
        show_main_menu(user_id)
    elif 'get_user_info' in call.data:
        partner_user_id = call.data.split(',')[1]
        name = user_names[partner_user_id]
        sex = 'Мужской' if user_sex[partner_user_id] == 'male' else 'Женский'
        age = str(user_age[partner_user_id])
        bot.send_message(user_id, 'Имя: ' + name + '\nПол: '+sex+'\nВозраст: '+age)
    elif 'send_message' in call.data:
        partner_user_id = call.data.split(',')[1]
        sent = bot.send_message(user_id, 'Введи текст сообщения')
        bot.register_next_step_handler(sent, lambda m: send_message(m, user_id, partner_user_id))
    elif 'share_desire' in call.data:
        partner_user_id = call.data.split(',')[1]
        key_list = list(user_nicknames.keys())
        val_list = list(user_nicknames.values())
        position = (val_list.index(partner_user_id))
        partner_nickname = key_list[position]
        user_partners[user_id] = partner_nickname
        bot.send_message(user_id, 'Отлично! Идем дальше...')
        show_desires(user_id)
    elif call.data == 'change_nickname':
        sent = bot.send_message(user_id, 'Укажи свой ник')
        bot.register_next_step_handler(sent, lambda m: edit_nickname(m, user_id))
    elif call.data == 'change_name':
        sent = bot.send_message(user_id, 'Укажи свое имя')
        bot.register_next_step_handler(sent, lambda m: edit_name(m, user_id))
    elif call.data == 'change_age':
        sent = bot.send_message(user_id, 'Укажи свой возраст')
        bot.register_next_step_handler(sent, lambda m: edit_age(m, user_id))
    elif call.data == 'change_sex':
        sex_keyboard = types.InlineKeyboardMarkup()
        key_male = types.InlineKeyboardButton(text='Мужской', callback_data='edit_sex_male')
        sex_keyboard.add(key_male)
        key_female = types.InlineKeyboardButton(text='Женский', callback_data='edit_sex_female')
        sex_keyboard.add(key_female)
        bot.send_message(user_id, text='Укажи свой пол', reply_markup=sex_keyboard)
    elif call.data == "edit_sex_male":
        user_sex[user_id] = 'male'
        bot.send_message(user_id, 'Пол обновлен')
        show_main_menu(user_id)
    elif call.data == "edit_sex_female":
        user_sex[user_id] = 'female'
        bot.send_message(user_id, 'Пол обновлен')
        show_main_menu(user_id)


def set_age(message, user_id):
    user_age[user_id] = message.text
    sent = bot.send_message(user_id, 'Введи свой уникальный ник, по которому пользователи смогут тебя найти')
    bot.register_next_step_handler(sent, lambda m: set_nickname(m, user_id))


def set_nickname(message, user_id):
    nickname = message.text.lower()
    if nickname in user_nicknames:
        sent = bot.send_message(user_id, 'Прости, но это имя уже занято. попробуй другое')
        bot.register_next_step_handler(sent, lambda m: set_nickname(m, user_id))
    else:
        user_nicknames[nickname] = user_id
    bot.send_message(user_id, 'Великолепно! Продолжим?')
    show_main_menu(user_id)


def edit_nickname(message, user_id):
    nickname = message.text.lower()
    if nickname in user_nicknames:
        sent = bot.send_message(user_id, 'Прости, но это имя уже занято. попробуй другое')
        bot.register_next_step_handler(sent, lambda m: edit_nickname(m, user_id))
    else:
        key_list = list(user_nicknames.keys())
        val_list = list(user_nicknames.values())
        position = (val_list.index(user_id))
        user_nickname = key_list[position]
        user_nicknames.pop(user_nickname)
        user_nicknames[nickname] = user_id
    bot.send_message(user_id, 'Твой ник изменен')
    show_main_menu(user_id)


def edit_name(message, user_id):
    name = message.text
    user_names[user_id] = name
    bot.send_message(user_id, 'Твое имя обновлено')
    show_main_menu(user_id)


def edit_age(message, user_id):
    age = message.text
    user_age[user_id] = age
    bot.send_message(user_id, 'Твой возраст обновлен')
    show_main_menu(user_id)


def input_partner(user_id):
    if user_sex[user_id] == 'male':
        text = 'Введи ник пользователя с которым ты хотел бы поделиться своими тайными желаниями'
    else:
        text = 'Введи ник пользователя с которым ты хотела бы поделиться своими тайными желаниями'
    sent = bot.send_message(user_id, text)
    bot.register_next_step_handler(sent, lambda m: set_partner(m, user_id))


def set_partner(message, user_id):
    partner_nickname = message.text.lower()
    if partner_nickname == 'exit':
        show_main_menu(user_id)
    elif partner_nickname in user_nicknames:
        partner_user_id = user_nicknames[partner_nickname]
        user_partners[user_id] = partner_nickname
        bot.send_message(user_id, 'Отлично! Идем дальше...')
        show_desires(user_id)
    else:
        sent = bot.send_message(user_id, 'Пользователь с таким ником не найден. Попробуй другой ник')
        bot.register_next_step_handler(sent, lambda m: set_partner(m, user_id))


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Пользователи":
        show_users(str(message.from_user.id))
    elif message.text == "Перейти к желаниям":
        input_partner(str(message.from_user.id))
    elif message.text == "Перейти к желаниям":
        input_partner(str(message.from_user.id))
    elif message.text == "Помощь":
        show_help(str(message.from_user.id))
    elif message.text == "Профиль":
        show_profile(str(message.from_user.id))
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


def show_desires(user_id):
    d_keyboard = types.InlineKeyboardMarkup()
    key_dinner = types.InlineKeyboardButton(text='Ужин вдвоем', callback_data='dinner')
    d_keyboard.add(key_dinner)
    key_cinema = types.InlineKeyboardButton(text='Поход в кино', callback_data='cinema')
    d_keyboard.add(key_cinema)
    key_massage = types.InlineKeyboardButton(text='Массаж', callback_data='massage')
    d_keyboard.add(key_massage)
    key_sex = types.InlineKeyboardButton(text='Секс', callback_data='sex')
    d_keyboard.add(key_sex)
    bot.send_message(user_id, text='Твои тайные желания станут известны пользователю с ником '+user_partners[user_id]+'\nЧего ты желаешь?\n', reply_markup=d_keyboard)


def generate_desires_markup():
    list_items = ['Ужин вдвоем', 'Массаж', 'Поход в кино', 'Секс', ]
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for item in list_items:
        markup.add(item)
    return markup


def show_main_menu(user_id):
    markup = generate_main_menu_markup()
    bot.send_message(user_id, text='Что дальше?', reply_markup=markup)


def show_users(user_id):
    for user in user_nicknames:
        id = user_nicknames[user]
        name = user_names[id]
        sex = 'Мужской' if user_sex[id] == 'male' else 'Женский'
        age = str(user_age[id])
        # bot.send_message(user_id, text='Ник: ' + user + '\nИмя: ' + name + '\nПол: '+sex+'\nВозраст: '+age)
        share_desire_keyboard = types.InlineKeyboardMarkup()
        key_share_desire = types.InlineKeyboardButton(text='Поделиться желанием', callback_data='share_desire,' + id)
        share_desire_keyboard.add(key_share_desire)
        bot.send_message(user_id, 'Ник: ' + user + '\nИмя: ' + name + '\nПол: '+sex+'\nВозраст: '+age, reply_markup=share_desire_keyboard)
    show_main_menu(user_id)


def generate_main_menu_markup():
    list_items = ['Пользователи', 'Перейти к желаниям', 'Профиль', 'Помощь', ]
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for item in list_items:
        markup.add(item)
    return markup


def show_help(user_id):
    bot.send_message(user_id, 'Страничка помощи в использовании бота Secret Desires.\n Команды:'
                              '\n/start - начать общение с ботом'
                              '\nexit - выйти из текущего модуля в главное меню')


def show_profile(user_id):
    key_list = list(user_nicknames.keys())
    val_list = list(user_nicknames.values())
    position = (val_list.index(user_id))
    user_nickname = key_list[position]
    change_nickname_keyboard = types.InlineKeyboardMarkup()
    key_change_nickname = types.InlineKeyboardButton(text='Изменить', callback_data='change_nickname')
    change_nickname_keyboard.add(key_change_nickname)
    bot.send_message(user_id, text='Ник: ' + user_nickname, reply_markup=change_nickname_keyboard)
    name = user_names[user_id]
    change_name_keyboard = types.InlineKeyboardMarkup()
    key_change_name = types.InlineKeyboardButton(text='Изменить', callback_data='change_name')
    change_name_keyboard.add(key_change_name)
    bot.send_message(user_id, text='Имя: ' + name, reply_markup=change_name_keyboard)
    sex = 'Мужской' if user_sex[user_id] == 'male' else 'Женский'
    change_sex_keyboard = types.InlineKeyboardMarkup()
    key_change_sex = types.InlineKeyboardButton(text='Изменить', callback_data='change_sex')
    change_sex_keyboard.add(key_change_sex)
    bot.send_message(user_id, text='Пол: ' + sex, reply_markup=change_sex_keyboard)
    age = str(user_age[user_id])
    change_age_keyboard = types.InlineKeyboardMarkup()
    key_change_age = types.InlineKeyboardButton(text='Изменить', callback_data='change_age')
    change_age_keyboard.add(key_change_age)
    bot.send_message(user_id, text='Возраст: ' + age, reply_markup=change_age_keyboard)


def send_message(message, user_id, partner_user_id):
    sender_name = user_names[user_id]
    m = message.text
    text = 'Сообщение от '+sender_name+'\n\n'+m
    reply_keyboard = types.InlineKeyboardMarkup()
    key_reply = types.InlineKeyboardButton(text='Ответить', callback_data='send_message,' + user_id)
    reply_keyboard.add(key_reply)
    bot.send_message(partner_user_id, text, reply_markup=reply_keyboard)


bot.polling(none_stop=True, interval=0)