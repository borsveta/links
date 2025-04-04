import telebot
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
ACCESS_CODE = "access2024"
LINKS_FILE = "links.txt"

bot = telebot.TeleBot(BOT_TOKEN)
user_links = {}  # Словарь для хранения выданных ссылок: {chat_id: link}

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
    chat_id = message.chat.id

    # Если команда содержит нужный параметр (access2024)
    if len(args) > 1 and args[1] == ACCESS_CODE:
        # Если для этого пользователя ссылка уже выдана, отправляем её повторно
        if chat_id in user_links:
            bot.send_message(chat_id, f"Ты уже получил свою ссылку:\n{user_links[chat_id]}")
        else:
            link = get_next_link()
            if link:
                user_links[chat_id] = link  # Сохраняем, что этому пользователю выдана ссылка
                bot.send_message(chat_id, f"Вот твоя уникальная ссылка:\n{link}")
            else:
                bot.send_message(chat_id, "Извините, ссылки закончились.")
    else:
        bot.send_message(chat_id,
            "Привет! Для доступа используй специальную ссылку после оплаты.\n" +
            "Например: http://t.me/linkmoro_bot?start=access2024"
        )

print("✅ Бот успешно запущен и слушает сообщения...")
bot.polling()
