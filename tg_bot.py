"""Module for work with python-telegram-bot."""

import json
import random

import redis
from environs import Env
from pathlib import Path
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
)

MENU_KEYBOARD = [
    ['Новый вопрос', 'Мой счет'],
    ['Закончить игру'],
    ]
ANSWER_KEYBOARD = [
    ['Сдаться'],
    ['Закончить игру'],
    ]

MENU_MARKUP = ReplyKeyboardMarkup(
    MENU_KEYBOARD,
    one_time_keyboard=True,
    resize_keyboard=True,
    )
ANSWER_MARKUP = ReplyKeyboardMarkup(
    ANSWER_KEYBOARD,
    one_time_keyboard=True,
    resize_keyboard=True,
)

MENU, GET_ANSWER = range(2)


def get_quiz_qna(json_path='questions.json'):
    """Load quiz questions and answers from JSON."""
    path = Path.cwd() / json_path
    with open(path, 'r', encoding='utf-8') as dump:
        quiz_qna = json.load(dump)

    return quiz_qna


def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    update.effective_chat.send_message(
        text='Привет! Я бот для викторин.',
        reply_markup=MENU_MARKUP,
        )

    return MENU


def new_question(update: Update, context: CallbackContext):
    """Send new question."""
    user_id = update.effective_user.id
    quiz_qna = context.bot_data['quiz_qna']
    question = random.choice(list(quiz_qna.keys()))   # noqa: S311
    database = context.bot_data['database']
    database.set(user_id, question)
    update.message.reply_text(question, reply_markup=ANSWER_MARKUP)

    return GET_ANSWER


def check_answer(update: Update, context: CallbackContext):
    """Check user answer."""
    user_id = update.effective_user.id
    database = context.bot_data['database']
    question = database.get(user_id)
    correct_answer = context.bot_data['quiz_qna'].get(question)
    user_answer = update.message.text

    if user_answer == correct_answer:
        update.message.reply_text('Верно!', reply_markup=MENU_MARKUP)
        return MENU
    else:
        update.message.reply_text(
            'Неверно. Попробуйте еще раз...', reply_markup=ANSWER_MARKUP,
            )
    return GET_ANSWER


def show_correct_answer(update: Update, context: CallbackContext):
    """Show correct answer to user."""
    user_id = update.effective_user.id
    database = context.bot_data['database']
    question = database.get(user_id)
    correct_answer = context.bot_data['quiz_qna'].get(question)
    update.message.reply_text(correct_answer, reply_markup=MENU_MARKUP)

    return MENU


def cancel(update: Update, context: CallbackContext):
    """Cancel conversation."""
    update.message.reply_text(
        'До встречи!', reply_markup=ReplyKeyboardRemove(),
        )

    return ConversationHandler.END


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
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            MENU: [
                MessageHandler(Filters.regex('^Новый вопрос'), new_question),
                MessageHandler(Filters.regex('^Закончить игру'), cancel),
                ],

            GET_ANSWER: [
                MessageHandler(Filters.regex('^Сдаться'), show_correct_answer),
                MessageHandler(Filters.regex('^Закончить игру'), cancel),
                MessageHandler(Filters.text, check_answer),
                ],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
