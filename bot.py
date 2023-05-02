"""Module for work with python-telegram-bot."""

import json
import random

import redis
from environs import Env
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)


def get_question(json_path='questions.json'):
    """Get random question-answer pair from JSON."""
    with open(json_path, 'r', encoding='utf-8') as dump:
        questions = json.load(dump)
        question = random.choice(list(questions.keys()))   # noqa: S311

    return question


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    custom_keyboard = [
        ['Новый вопрос', 'Сдаться'],
        ['Мой счет'],
        ]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    update.effective_chat.send_message(
        text='Привет! Я бот для викторин.',
        reply_markup=reply_markup,
        )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def new_question(update: Update, context: CallbackContext) -> None:
    """Send new question."""
    user_id = update.effective_user.id
    question = get_question()
    database = context.bot_data['database']
    database.set(user_id, question)
    update.message.reply_text(question)


def main() -> None:     # noqa: WPS210
    """Start the bot."""
    env = Env()
    env.read_env()
    tg_token = env.str('TG_BOT_TOKEN')
    redis_host = env.str('REDIS_HOST')
    redis_port = env.str('REDIS_PORT')
    redis_password = env.str('REDIS_PASSWORD')
    database = redis.Redis(
        host=redis_host,
        port=redis_port,
        password=redis_password,
        charset='utf-8',
        decode_responses=True,
    )
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data['database'] = database
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(
        MessageHandler(Filters.text('Новый вопрос'), new_question),
        )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
