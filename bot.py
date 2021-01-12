import config
import telebot
from telebot import types


bot = telebot.TeleBot(config.token)
user_names = {'185542622': 'Serg'}
user_sex = {'185542622': 'male'}
user_age = {'185542622': 35}
user_nicknames = {'g00dvveen': '185542622'}
user_partners = {'185542622': 'g00dvveen'}


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = str(message.from_user.id)
    if user_id in user_names:
        bot.send_message(user_id, 'Привет, '+user_names[user_id])
        input_partner(user_id)
    else:
        sent = bot.send_message(user_id, 'Давай знакомиться! Как тебя зовут?')
        bot.register_next_step_handler(sent, lambda m: acquaint(m, user_id))


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
    key_list = list(user_nicknames.keys())
    val_list = list(user_nicknames.values())
    position = (val_list.index(user_id))
    user_nickname = key_list[position]
    if call.data == "set_sex_male":
        user_sex[user_id] = 'male'
        sent = bot.send_message(user_id, 'Отлично! Сколько тебе лет?')
        bot.register_next_step_handler(sent, lambda m: set_age(m, user_id))
    elif call.data == "set_sex_female":
        user_sex[user_id] = 'female'
        sent = bot.send_message(user_id, 'Отлично! Сколько тебе лет?')
        bot.register_next_step_handler(sent, lambda m: set_age(m, user_id))
    elif call.data == "dinner":
        partner_nickname = user_partners[user_id]
        partner_user_id = user_nicknames[partner_nickname]
        bot.send_message(partner_user_id, 'Пользователь с ником '+user_nickname+' желает с тобой поужинать!')
        get_info_keyboard = types.InlineKeyboardMarkup()
        key_get_info = types.InlineKeyboardButton(text='Показать', callback_data='get_user_info,'+partner_user_id)
        get_info_keyboard.add(key_get_info)
        bot.send_message(partner_user_id, 'Показать профиль', reply_markup=get_info_keyboard)
    elif call.data == "cinema":
        partner_nickname = user_partners[user_id]
        partner_user_id = user_nicknames[partner_nickname]
        bot.send_message(partner_user_id, 'Пользователь с ником '+user_nickname+' желает сходить с тобой! в кино')
        get_info_keyboard = types.InlineKeyboardMarkup()
        key_get_info = types.InlineKeyboardButton(text='Показать', callback_data='get_user_info,' + partner_user_id)
        get_info_keyboard.add(key_get_info)
        bot.send_message(partner_user_id, 'Показать профиль', reply_markup=get_info_keyboard)
    elif call.data == "massage":
        partner_nickname = user_partners[user_id]
        partner_user_id = user_nicknames[partner_nickname]
        bot.send_message(partner_user_id, 'Пользователь с ником '+user_nickname+' желает получить от тебя массаж!')
        get_info_keyboard = types.InlineKeyboardMarkup()
        key_get_info = types.InlineKeyboardButton(text='Показать', callback_data='get_user_info,' + partner_user_id)
        get_info_keyboard.add(key_get_info)
        bot.send_message(partner_user_id, 'Показать профиль', reply_markup=get_info_keyboard)
    elif call.data == "sex":
        partner_nickname = user_partners[user_id]
        partner_user_id = user_nicknames[partner_nickname]
        bot.send_message(partner_user_id, 'Пользователь с ником '+user_nickname+' желает секса с тобой!')
        get_info_keyboard = types.InlineKeyboardMarkup()
        key_get_info = types.InlineKeyboardButton(text='Показать', callback_data='get_user_info,' + partner_user_id)
        get_info_keyboard.add(key_get_info)
        bot.send_message(partner_user_id, 'Показать профиль', reply_markup=get_info_keyboard)
    elif 'get_user_info' in call.data:
        partner_user_id = call.data.split(',')[1]
        name = user_names[user_id]
        sex = 'Мужской' if user_sex[user_id] == 'male' else 'Женский'
        age = str(user_age[user_id])
        bot.send_message(partner_user_id, 'Имя: ' + name + '\nПол: '+sex+'\nВозраст: '+age)

def set_age(message, user_id):
    user_age[user_id] = int(message.text)
    sent = bot.send_message(user_id, 'Введи свой уникальный ник, по которому пользователи смогут тебя найти')
    bot.register_next_step_handler(sent, lambda m: set_nickname(m, user_id))


def set_nickname(message, user_id):
    nickname = message.text.lower()
    if user_id in user_nicknames:
        sent = bot.send_message(user_id, 'Прости, но это имя уже занято. попробуй другое')
        bot.register_next_step_handler(sent, lambda m: set_nickname(m, user_id))
    else:
        user_nicknames[nickname] = user_id
    bot.send_message(user_id, 'Великолепно! Продолжим?')
    input_partner(user_id)


def input_partner(user_id):
    if user_sex[user_id] == 'male':
        text = 'Введи ник пользователя с которым ты хотел бы поделиться своими тайными желаниями'
    else:
        text = 'Введи ник пользователя с которым ты хотела бы поделиться своими тайными желаниями'
    sent = bot.send_message(user_id, text)
    bot.register_next_step_handler(sent, lambda m: set_partner(m, user_id))


def set_partner(message, user_id):
    partner_nickname = message.text.lower()
    if partner_nickname in user_nicknames:
        partner_user_id = user_nicknames[partner_nickname]
        user_partners[user_id] = partner_nickname
        bot.send_message(user_id, 'Отлично! Идем дальше...')
        show_desires(user_id)
    else:
        sent = bot.send_message(user_id, 'Пользователь с таким ником не найден. Попробуй другой ник')
        bot.register_next_step_handler(sent, lambda m: set_partner(m, user_id))


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, сейчас я расскажу тебе гороскоп на сегодня.")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши Привет")
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

bot.polling(none_stop=True, interval=0)
