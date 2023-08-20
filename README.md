# Quiz bots for VK and Telegram
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
___

You can see how the bots is working by visiting [@dvmn-test](http://t.me/dvmn_misc_bot) for telegram and [DVMN-bot](https://vk.com/club219791098) for VK.

## How to install:
1. Python 3 should be already installed
2. Download repository 
3. Install dependencies by running
```bash
python3 -m pip install -r requirements.txt
```

## Setting up:

For use this scripts, you will need:
- Telegram bot token (use existing one or create new on [@BotFather](http://t.me/BotFather))
- Your Telegram chat ID (use [@userinfobot](tg://resolve?domain=userinfobot) if you don't know where to look for ID)
- Your Redis credentials - host, port and password. To obtain, login to [Redislabs](https://redislabs.com/), create new database and use provided credentials.
- Your VK group token (for using VK bot). Create group [here](https://vk.com/groups_create), in group `Settings - Messages - Bot settings` enable `Bot abilities`, then in `Settings - API usage` create token.

Create .env file and fill it with variables as in env_example file.

## Create quiz questions from text files:

Download [archive](https://dvmn.org/media/modules_dist/quiz-questions.zip) with questions and answers. Place all text files with questions and answers in `quiz/` directory inside project directory, then run
```bash
python3 make_questions.py
```
Script will generate JSON file with quiz QnA.

## Running scripts:

To use telegram bot, type

```bash
python3 tg_bot.py
```

To use VK bot, type

```bash
python3 vk_bot.py
```

## Project goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/)
