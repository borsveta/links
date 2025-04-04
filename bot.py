import telebot
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Токен берется из переменной окружения
ACCESS_CODE = "access2024"
LINKS_FILE = "links.txt"

bot = telebot.TeleBot(BOT_TOKEN)

def get_next_link():
    with open(LINKS_FILE, "r") as f:
        links = f.readlines()

    if not links:
        return None

    next_link = links[0].strip()
    remaining = links[1:]

    with open(LINKS_FILE, "w") as f:
        f.writelines(remaining)

    return next_link

@bot.message_handler(commands=['start'])
def handle_start(message):
    args = message.text.split()
    if len(args) > 1 and args[1] == ACCESS_CODE:
        link = get_next_link()
        if link:
            bot.send_message(message.chat.id, f"Вот твоя уникальная ссылка для доступа к курсу:\n{link}")
        else:
            bot.send_message(message.chat.id, "Извините, ссылки закончились. Напишите нам для получения доступа.")
    else:
        bot.send_message(message.chat.id, "Привет! Для доступа к курсу используй специальную ссылку после оплаты.")

bot.polling()
