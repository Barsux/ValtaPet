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


dicts = read_json('dialog1.json')
saved = None
num = 0

def get_buttons(buttons_dict: list) -> list:
    rows = []
    for dicts in buttons_dict:
        row = []
        for text in dicts["texts"]:
            row.append(telebot.types.KeyboardButton(text=text))
        rows.append(row)
    return rows


@bot.message_handler(commands=['start'])
def start(message):
    text = dicts["reply"]
    keyboard = telebot.types.ReplyKeyboardMarkup()
    buttons_rows = get_buttons(dicts["buttons"])
    for button_row in buttons_rows:
        keyboard.add(*button_row)
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

@bot.message_handler(content_types='text')
def reply(message):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    reply = message.text
    dialogs = dicts["dialogs"]
    for dialog in dialogs:
        if dialog["num"] != num: continue
        text = dialog["text"]
        saved  = dialog["buttons"]



bot.polling()
