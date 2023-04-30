"""Module for work with python-telegram-bot."""
from environs import Env
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)


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


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


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
        MessageHandler(Filters.text and ~Filters.command, echo),
        )
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
