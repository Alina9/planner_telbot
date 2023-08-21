import sys
import telebot
import openai
from collections import OrderedDict

TOKEN = ""  # Telegram bot's token
ALLOWED_TELEGRAM_USER_IDS = "*"
HELP = """
* help - print program info.
* add {dd.mm.yy} {task} - add task in the list.
* show {dd.mm.yy} - print all added tasks this date.
* show_all -  print all added tasks.
"""

bot = telebot.TeleBot(TOKEN)
tasks = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hi! This is your planner! Write /help for some additional info")


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['add'])
def send_add(message):
    _, date, task = message.text.split(maxsplit=2)
    if date in tasks:
        if task in tasks[date]:
            bot.send_message(message.chat.id, 'This date and task have already been added!')
        else:
            tasks[date] += [task]
            bot.send_message(message.chat.id, "Task was added!")
    else:
        tasks[date] = [task]
        bot.send_message(message.chat.id, "Task was added!")


@bot.message_handler(commands=['show_all'])
def send_show_all(message):
    text = ''
    for d in tasks:
        text += f"Date: {d} \n"
        for i, t in enumerate(tasks[d]):
            text += f"{i + 1}) {t} \n"
        text += "\n"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['show'])
def send_show_date(message):
    _, date = message.text.split(maxsplit=1)
    text = ''
    if date in tasks:
        text += f"Date: {date} \n"
        for i, t in enumerate(tasks[date]):
            text += f"{i + 1}) {t} \n"
    else:
        text = f"You don't have task on {date}"
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message.chat.id,
                 "Sorry, I don't understand you. I know only few commands. Write /help and check them.")


if __name__ == "__main__":
    bot.infinity_polling()


