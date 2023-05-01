"""Module for work with python-telegram-bot."""

import json
import random

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
        question = random.choice(list(questions.items()))   # noqa: S311

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
    question, answer = get_question()
    update.message.reply_text(question)


def main() -> None:
    """Start the bot."""
    env = Env()
    env.read_env()
    tg_token = env.str('TG_BOT_TOKEN')
    updater = Updater(tg_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(
        MessageHandler(Filters.text('Новый вопрос'), new_question),
        )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
