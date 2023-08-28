import json
from pathlib import Path


def get_quiz_qna(json_path='questions.json'):
    """Load quiz questions and answers from JSON."""
    path = Path.cwd() / json_path
    with open(path, 'r', encoding='utf-8') as dump:
        quiz_qna = json.load(dump)

    return quiz_qna
