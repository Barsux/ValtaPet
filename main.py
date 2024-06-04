import json
import telebot

bot = telebot.TeleBot("7350145332:AAH8zpY8Lsk6fjMkvPM3Nk0oYrEyVwzdEtw", parse_mode=None)


def read_json(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError or FileExistsError or json.JSONDecodeError as e:
        pass
    return None



@bot.message_handler(commands=['start'])
def start(message):
    keyboard=telebot.types.ReplyKeyboardMarkup()
    button1 = telebot.types.KeyboardButton(text="Ёж")
    button2 = telebot.types.KeyboardButton(text="Жук")
    button3 = telebot.types.KeyboardButton(text="Боевой вертолёт Ка52")
    keyboard.add(button1, button2, button3)
    bot.send_message(chat_id=message.chat.id, text="Кто ты по жизни?", reply_markup=keyboard)


#bot.polling()
print(read_json('dialogs.json'))