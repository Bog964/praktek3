import telebot
from telebot import types
import random

TOKEN = '7386296655:AAFtqpH-hRR-kALatsb2x7_H5nOsLkI-Kzw'
bot = telebot.TeleBot(TOKEN)

questions = {
    "Як звати винахідника Python?": "Гвідо ван Россум",
    "Що таке змінна?": "Місце для зберігання даних",
    "Який оператор використовується для обчислення остачі?": "%"
}

@bot.message_handler(commands=["start"])
def send_start(message):
    bot.send_message(message.chat.id, "Привіт! Я бот, що задає питання. Використовуй /help для списку команд!")

@bot.message_handler(commands=["help"])  # Виправлено назву команди
def send_help(message):
    bot.send_message(message.chat.id, "Ось список доступних команд:\n"
                                      "/start - Розпочати роботу\n"
                                      "/help - Отримати список команд\n"
                                      "/question - Отримати випадкове запитання\n"
                                      "/add - Додати своє запитання\n"
                                      "/fact - Цікавий факт про програмування\n"
                                      "/info - Інформація про бота\n"
                                      "/about - Щось цікаве!")

@bot.message_handler(commands=["info"])
def send_info(message):
    bot.send_message(message.chat.id, "Я бот, який може задати питання або дозволити додати свої!")

@bot.message_handler(commands=["about"])  # Доданий декоратор
def send_about(message):
    bot.send_message(message.chat.id, "Факт: Python був створений як проста мова для початківців, а тепер його використовують по всьому світу.")

@bot.message_handler(commands=["question"])
def send_question(message):
    if questions:
        question = random.choice(list(questions.keys()))
        bot.send_message(message.chat.id, f"Ось твоє питання: {question}")
        bot.register_next_step_handler(message, check_answer, question)
    else:
        bot.send_message(message.chat.id, "Питань поки що немає. Ви можете додати їх за допомогою команди /add.")

def check_answer(message, question):
    user_answer = message.text.strip().lower()
    correct_answer = questions[question].strip().lower()
    if user_answer == correct_answer:
        bot.reply_to(message, "Правильно, молодець!")
    else:
        bot.reply_to(message, f"Неправильно. Правильна відповідь: {questions[question]}")

@bot.message_handler(commands=["add"])
def add_question(message):
    bot.send_message(
        message.chat.id,
        "Напишіть питання у форматі: питання - відповідь"
    )
    bot.register_next_step_handler(message, save_question)

def save_question(message):
    try:
        question, answer = message.text.split(" - ")
        questions[question.strip()] = answer.strip()
        bot.reply_to(message, "Запитання додано!")
    except ValueError:
        bot.reply_to(
            message,
            "Будь ласка, використовуйте формат: питання - відповідь"
        )

@bot.message_handler(commands=["fact"])
def send_fact(message):
    facts = [  # Виправлено назву змінної
        "Python використовують NASA для аналізу даних.",
        "Facebook, Instagram і YouTube активно використовують Python.",
        "Перша комп'ютерна гра була створена у 1961 році."
    ]
    bot.send_message(message.chat.id, random.choice(facts))

@bot.message_handler(commands=["menu"])
def send_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn_question = types.KeyboardButton('question')
    btn_add = types.KeyboardButton('add')
    btn_fact = types.KeyboardButton('fact')
    btn_info = types.KeyboardButton('info')
    markup.add(btn_question, btn_add, btn_fact, btn_info)
    bot.send_message(message.chat.id, "Ось твоє меню:", reply_markup=markup)

bot.polling()
