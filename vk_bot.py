"""Module for work with vk bot."""

import json
import random

import redis
import vk_api as vk
from environs import Env
from pathlib import Path
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkEventType, VkLongPoll


def get_quiz_qna(json_path='questions.json'):
    """Load quiz questions and answers from JSON."""
    path = Path.cwd() / json_path
    with open(path, 'r', encoding='utf-8') as dump:
        quiz_qna = json.load(dump)

    return quiz_qna


def send_message(event, vk_api, messaage, keyboard):
    """Send message to user."""
    vk_api.messages.send(
        user_id=event.user_id,
        message=messaage,
        random_id=random.randint(1, 1000),  # noqa: S311
        keyboard=keyboard.get_keyboard(),
    )


def handle_quiz(event, vk_api, database, quiz_qna, keyboard):
    """Handle interaction with user."""
    if event.text == 'Новый вопрос':
        question = random.choice(list(quiz_qna.keys()))     # noqa: S311
        database.set(event.user_id, question)
        send_message(event, vk_api, question, keyboard)
    elif event.text == 'Сдаться':
        question = database.get(event.user_id)
        correct_answer = quiz_qna.get(question)
        send_message(event, vk_api, correct_answer, keyboard)
    else:
        question = database.get(event.user_id)
        user_answer = event.text
        correct_answer = quiz_qna.get(question)

        if user_answer == correct_answer:
            message = 'Верно!'
            send_message(event, vk_api, message, keyboard)
        else:
            message = 'Неверно. Попробуйте еще раз...'
            send_message(event, vk_api, message, keyboard)


def main() -> None:     # noqa: WPS210
    """Start the bot."""
    env = Env()
    env.read_env()
    vk_token = env.str('VK_TOKEN')
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

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            handle_quiz(
                event,
                vk_api,
                database,
                quiz_qna,
                keyboard,
            )


if __name__ == '__main__':
    main()
