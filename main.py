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


dicts = read_json('dialogs.json')
saved = None
num = 0
attributes = {}
for attr in dicts["attributes"]:
    attributes[attr] = 0
attributes["exceptions"] = []
print(attributes)


def get_buttons(buttons_dict: list) -> list:
    rows = []
    row = None
    for button_row in buttons_dict:
        row = list(map(lambda button: list(button.keys())[0], button_row))
        rows.append(row)
    return rows


def parse_dialog(num):
    text = None
    keyboard = telebot.types.ReplyKeyboardMarkup()
    for dialog in dicts["dialogs"]:
        if dialog["num"] != num: continue
        text = dialog["reply"]
        buttons = get_buttons(dialog["buttons"])
        for row in buttons:
            keyboard.add(*row)
        save = dialog["buttons"]
    return text, keyboard, save


def end_script(message):
    global attributes
    print(attributes)

@bot.message_handler(commands=['start'])
def start(message):
    global num, saved
    text, keyboard, save = parse_dialog(0)
    bot.send_message(message.chat.id, text, reply_markup=keyboard)
    num = 1
    saved  = save



@bot.message_handler(content_types='text')
def reply(message):
    global num, dicts, attributes, saved
    text, keyboard, saves = parse_dialog(num)
    num += 1
    bot.send_message(message.chat.id, text, reply_markup=keyboard)
    msg = message.text
    if num == dicts["end"]:
        print(attributes)
        return
    if saved:
        saved = list(map(lambda button: button[0], saved))
    print(saved)
    for save in saved:
        if msg not in save: continue
        key, value = msg, save[msg]
        if "exceptions: " in value:
            value = value.replace("exceptions:  ", "")
            value  = value.split(",")
            value  = list(map(lambda x: x.strip(), value))
            for val in value:
                if '-' in val:
                    val = val.replace("-",  "")
                    attributes["exceptions"].remove(val)
                else:
                    attributes["exceptions"].append(val)
        else:
            for val in value:
                isNegative = '-' in val
                print(val)
                attr, digit = val.split('-' if isNegative else '+')
                if  attr not in attributes:
                    continue
                attributes[attr]  += (int(digit) * -1 if isNegative else 1)


bot.polling()
