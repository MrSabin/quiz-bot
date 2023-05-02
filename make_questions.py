"""Module for get questions and answers from text files."""

import json
import os
from pathlib import Path


def scan_folder() -> list:
    """Scan folder for files, return list of files."""
    path = Path.cwd() / 'quiz'
    filepaths = []
    files = os.listdir(path)

    for text_file in files:
        filepaths.append(os.path.join(path, text_file))

    return filepaths


def split_text(filepath: str) -> list:
    """Open text file, split it, return list of strings."""
    with open(filepath, 'r', encoding='KOI8-R') as text_file:
        return text_file.read().split('\n\n')


def format_questions(splitted_text: list) -> dict:
    """Return dict with formatted questions."""
    questions_part = {}
    question = ''
    answer = ''

    for phrase in splitted_text:
        if 'Вопрос ' in phrase:
            question = phrase.partition(':\n')[2].replace('\n', ' ')
        elif 'Ответ' in phrase:
            answer = phrase.partition(':\n')[2].replace('\n', ' ')
        questions_part[question] = format_answer(answer)

    return questions_part


def format_answer(answer: str) -> str:
    """Format answer, exclude explanations."""
    if '(' in answer:
        formatted_answer = answer.partition('(')[0]
    else:
        return answer.strip(' ."')

    return formatted_answer.strip(' ."')


def write_json(questions) -> None:
    """Save questions in JSON file."""
    filepath = Path.cwd() / 'questions.json'
    with open(filepath, 'w') as dump:
        json.dump(questions, dump, ensure_ascii=False, indent=4)


def main():  # noqa: D103
    filepaths = scan_folder()
    quiz_questions = {}

    for filepath in filepaths:
        splitted_text = split_text(filepath)
        questions_part = format_questions(splitted_text)
        quiz_questions.update(questions_part)

    write_json(quiz_questions)


if __name__ == '__main__':
    main()
