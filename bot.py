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

reply_keyboard = [
    ['Новый вопрос', 'Сдаться'],
    ['Мой счет'],
    ]
markup = ReplyKeyboardMarkup(
    reply_keyboard,
    one_time_keyboard=True,
    resize_keyboard=True,
    )

NEW_QUESTION, GET_ANSWER, GIVE_UP, MY_STATS = range(4)


def get_quiz_qna(json_path='questions.json'):
    """Load quiz questions and answers from JSON."""
    with open(json_path, 'r', encoding='utf-8') as dump:
        quiz_qna = json.load(dump)

    return quiz_qna


def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.effective_chat.send_message(
        text='Привет! Я бот для викторин.',
        reply_markup=markup,
        )


def new_question(update: Update, context: CallbackContext) -> None:
    """Send new question."""
    user_id = update.effective_user.id
    quiz_qna = context.bot_data['quiz_qna']
    question = random.choice(list(quiz_qna.keys()))   # noqa: S311
    database = context.bot_data['database']
    database.set(user_id, question)
    update.message.reply_text(question, reply_markup=markup)


def check_answer(update: Update, context: CallbackContext) -> None:
    """Check user answer."""
    user_id = update.effective_user.id
    database = context.bot_data['database']
    question = database.get(user_id)
    correct_answer = context.bot_data['quiz_qna'].get(question)
    user_answer = update.message.text

    if user_answer == correct_answer:
        update.message.reply_text('Верно!', reply_markup=markup)
    else:
        update.message.reply_text(
            'Неверно. Попробуйте еще раз...', reply_markup=markup,
            )


def show_correct_answer(update: Update, context: CallbackContext) -> None:
    """Show correct answer to user."""
    user_id = update.effective_user.id
    database = context.bot_data['database']
    question = database.get(user_id)
    correct_answer = context.bot_data['quiz_qna'].get(question)
    update.message.reply_text(correct_answer, reply_markup=markup)


def main() -> None:     # noqa: WPS210
    """Start the bot."""
    env = Env()
    env.read_env()
    tg_token = env.str('TG_BOT_TOKEN')
    redis_host = env.str('REDIS_HOST')
    redis_port = env.str('REDIS_PORT')
    redis_password = env.str('REDIS_PASSWORD')
    quiz_qna = get_quiz_qna()
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
    dispatcher.bot_data['quiz_qna'] = quiz_qna
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(
        MessageHandler(Filters.text('Новый вопрос'), new_question),
        )
    dispatcher.add_handler(
        MessageHandler(Filters.text('Сдаться'), show_correct_answer),
        )
    dispatcher.add_handler(
        MessageHandler(Filters.text, check_answer),
        )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
