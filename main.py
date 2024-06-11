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
    print(rows)
    return rows


def parse_dialog(num):
    global saved
    text = None
    keyboard = telebot.types.ReplyKeyboardMarkup()
    for dialog in dicts["dialogs"]:
        if dialog["num"] != num: continue
        text = dialog["reply"]
        buttons = get_buttons(dialog["buttons"])
        for row in buttons:
            keyboard.add(*row)
        saved = dialog["buttons"]
    print(text)
    return text, keyboard


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

            if "exc" in action:
                action = action.split(": ")[1]
                if ',' in action:
                    action.split(',')
                else:
                    action = [action]
                action = list(map(lambda acts: acts.strip(), action))
                for act in action:
                    isNegative  =  "-" in act
                    act = act.replace('+', '').replace('-', '')
                    if isNegative:
                        attributes["exceptions"].remove(act)
                    else:
                        attributes["exceptions"].append(act)
            else:
                isNegative = "-" in action
                act, value = action.split('-') if isNegative else action.split('+')
                if act in attributes:
                    if isNegative:
                        attributes[act] -= int(value)
                    else:
                        attributes[act] += int(value)



bot.polling()
