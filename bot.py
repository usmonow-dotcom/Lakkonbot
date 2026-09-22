import telebot

bot = telebot.TeleBot("8970808690:AAHpSXLaDk1knzJ3mnMKFuJETFfqEAm8bqs")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    bot.reply_to(message, "⏳ Скачиваю видео...")

    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("video.mp4", "wb") as f:
        f.write(downloaded_file)

    bot.send_video(message.chat.id, open("video.mp4", "rb"))

@bot.message_handler(func=lambda message: True)
def reply(message):
    bot.reply_to(message, "Привет! Я работаю. Отправь мне видео 🎥")

bot.infinity_polling()