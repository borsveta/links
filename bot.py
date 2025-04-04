import telebot
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
LINKS_FILE = "links.txt"

bot = telebot.TeleBot(BOT_TOKEN)
user_links = {}  # Словарь для хранения выданных ссылок: {chat_id: ссылка}

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
    chat_id = message.chat.id
    # Если пользователю уже выдана ссылка, повторно её отправляем
    if chat_id in user_links:
        bot.send_message(chat_id, f"Вот ваша ссылка для доступа к курсу:\n{user_links[chat_id]}")
    else:
        link = get_next_link()
        if link:
            user_links[chat_id] = link
            bot.send_message(chat_id, f"Вот ваша ссылка для доступа к курсу:\n{link}")
        else:
            bot.send_message(chat_id, "Извините, ссылки закончились.")

# Опционально: команда для просмотра количества оставшихся ссылок
@bot.message_handler(commands=['stats'])
def handle_stats(message):
    chat_id = message.chat.id
    try:
        with open(LINKS_FILE, "r") as f:
            links = f.readlines()
        count = len(links)
        bot.send_message(chat_id, f"Осталось ссылок: {count}")
    except Exception as e:
        bot.send_message(chat_id, f"Ошибка при чтении файла: {e}")

print("✅ Бот успешно запущен и слушает сообщения...")
bot.polling()
