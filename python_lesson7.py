import ptbot
import os
import random


from pytimeparse import parse
from dotenv import load_dotenv


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def reply(chat_id, message):
    sec = parse(message)
    message_id = BOT.send_message(chat_id, "Запускаю таймер!")
    BOT.create_countdown(sec, notify_progress, chat_id=chat_id, message_id=message_id, sec = sec)
    BOT.create_timer(sec, timer, chat_id=chat_id, message=message)


def notify_progress(secs_left,chat_id, message_id, sec):
    progressbar = render_progressbar(sec, sec - secs_left)
    message = "Осталось секунд: {}".format(secs_left)
    display = f'{message}\n{progressbar}'
    BOT.update_message(chat_id, message_id, display)


def timer(chat_id, message):
    message = "Время вышло!"
    BOT.send_message(chat_id, message)


def main():
    load_dotenv()
    TG_TOKEN = os.environ['TG_TOKEN']
    global BOT 
    BOT = ptbot.Bot(TG_TOKEN)
    BOT.reply_on_message(reply)
    BOT.run_bot()


if __name__ == '__main__':
    main()
