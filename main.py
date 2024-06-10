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
attributes = {}
for attr in dicts["attributes"]:
    attributes[attr] = 0
attributes["exceptions"] = []
print(attributes)

def get_buttons(buttons_dict: list) -> list:
    rows = []
    row = None
    for button_row in buttons_dict:
        row = list(map(lambda dct: list(dct.keys())[0], button_row))
    if row: rows.append(row)
    return rows


def parse_dialog(num):
    global saved
    for dialog in dicts["dialogs"]:
        if dialog["num"] != num: continue
        text = dialog["reply"]
        keyboard = telebot.types.ReplyKeyboardMarkup()
        buttons = get_buttons(dialog["buttons"])
        for row in buttons:
            keyboard.add(*row)
        saved = dialog["buttons"]
        return text, keyboard
    else:
        return None


@bot.message_handler(commands=['start'])
def start(message):
    global num
    text, keyboard = parse_dialog(0)
    bot.send_message(message.chat.id, text, reply_markup=keyboard)
    num = 1



@bot.message_handler(content_types='text')
def reply(message):
    global num
    text, keyboard = parse_dialog(num)
    num += 1
    bot.send_message(message.chat.id, text, reply_markup=keyboard)
    msg = message.text
    for savers in saved:
        if msg not in savers: continue
        for action in savers[msg]:
            isNegative = "-" in action
            act, value = action.split('-') if isNegative else action.split('+')
            if "exc" in action:
                if isNegative:
                    #remove act from attributes
                    attributes["exceptions"].remove(act)
                else:
                    attributes["exceptions"].append(act)
            else:
                if act in attributes:
                    if isNegative:
                        attributes[act] -= int(value)
                    else:
                        attributes[act] += int(value)



bot.polling()
