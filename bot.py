import telebot

bot = telebot.TeleBot("8970808690:AAHpSXLaDk1knzJ3mnMKFuJETFfqEAm8bqs")

@bot.message_handler(content_types=['video'])
def handle_video(message):
    bot.reply_to(message, "🎥 Видео получил! Готов обработать.")

@bot.message_handler(func=lambda message: True)
def reply(message):
    bot.reply_to(message, "Привет! Я работаю. Отправь мне видео 🎥")

bot.infinity_polling()