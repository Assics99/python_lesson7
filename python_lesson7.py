import ptbot
import os
import random

from decouple import config
from pytimeparse import parse
from dotenv import load_dotenv


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def reply(chat_id, message, bot):
    sec = parse(message)
    message_id = bot.send_message(chat_id, "Запускаю таймер!")
    bot.create_countdown(sec, notify_progress, chat_id=chat_id, message_id=message_id, sec = sec, bot = bot)
    bot.create_timer(sec, timer, chat_id=chat_id, message=message, bot = bot)


def notify_progress(secs_left,chat_id, message_id, sec, bot):
    progressbar = render_progressbar(sec, sec - secs_left)
    message = "Осталось секунд: {}".format(secs_left)
    display = f'{message}\n{progressbar}'
    bot.update_message(chat_id, message_id, display)


def timer(chat_id, message, bot):
    message = "Время вышло!"
    bot.send_message(chat_id, message)


def main():
    load_dotenv()
    tg_token = os.environ['TG_TOKEN'] 
    bot = ptbot.Bot(tg_token)
    bot.reply_on_message(reply, bot = bot)
    bot.run_bot()


if __name__ == '__main__':
    main()
