import os  # noqa: D100
from pathlib import Path


def scan_folder() -> list:
    """
    Scan folder for files.

    Returns:
        List of filepaths.
    """
    path = Path.cwd() / 'quiz'
    filepaths = []
    files = os.listdir(path)

    for text_file in files:
        filepaths.append(os.path.join(path, text_file))

    return filepaths


def split_text(filepath: str) -> list:
    """
    Open text file, split it, return list of strings.

    Args:
        filepath: filepath to use.

    Returns:
        List of strings.
    """
    with open(filepath, 'r', encoding='KOI8-R') as text_file:
        return text_file.read().split('\n\n')


def format_questions(splitted_text: list) -> dict:
    """
    Get questions and answers from list, format them.

    Args:
        splitted_text: text to use.

    Returns:
        Dict containing questions and answers.
    """
    questions_part = {}
    question = ''
    answer = ''

    for phrase in splitted_text:
        if 'Вопрос' in phrase:
            question = phrase.partition(':\n')[2].replace('\n', ' ')
        elif 'Ответ' in phrase:
            answer = phrase.partition(':\n')[2].replace('\n', ' ')
        questions_part[question] = answer

    return questions_part


def main():
    filepaths = scan_folder()
    quiz_questions = {}

    for filepath in filepaths:
        splitted_text = split_text(filepath)
        questions_part = format_questions(splitted_text)
        quiz_questions.update(questions_part)


if __name__ == '__main__':
    main()
