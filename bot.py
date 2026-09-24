import asyncio 
import os

--- ПАТЧ ДЛЯ СОВМЕСТИМОСТИ PILLOW И MOVIEPY ---
import PIL 
from PIL import Image 
if not hasattr(Image, 'ANTIALIAS'): 
Image.ANTIALIAS = Image.LANCZOS
---------------------------------------------

from aiogram import Bot, Dispatcher, F, types 
from aiogram.filters import Command 
from aiogram.fsm.storage.memory import MemoryStorage 
from moviepy.editor import VideoFileClip

Замените 'ВАШ_TELEGRAM_BOT_TOKEN' на ваш реальный токен
TOKEN = '8990434273:AAEPAZBWUyFHMRQDlH3VzpvTZFszWSUfbAE'

bot = Bot(token=TOKEN) 
storage = MemoryStorage() 
dp = Dispatcher(storage=storage)

DOWNLOAD_DIR = 'downloads' 
OUTPUT_DIR = 'output' 
os.makedirs(DOWNLOAD_DIR, exist_ok=True) 
os.makedirs(OUTPUT_DIR, exist_ok=True)

@dp.message(Command("start")) 
async def cmd_start(message: types.Message): 
await message.answer("Привет! Отправь мне короткое видео (до 15 МБ), и я сделаю из него вертикальный ролик!")

@dp.message(F.video) 
async def handle_video(message: types.Message): 
if message.video.file_size > 15 * 1024 * 1024: 
await message.answer("Файл слишком большой! Пожалуйста, отправьте видео весом меньше 15 МБ.") 
return

await message.answer("Видео получено! Скачиваю...")

file_id = message.video.file_id
file_info = await bot.get_file(file_id)
file_path = file_info.file_path

input_video_path = os.path.join(DOWNLOAD_DIR, f"{file_id}.mp4")
output_video_path = os.path.join(OUTPUT_DIR, f"{file_id}_result.mp4")

success = False
for attempt in range(3):
    try:
        await bot.download_file(file_path, input_video_path, timeout=60)
        success = True
        break
    except Exception as e:
        print(f"Попытка {attempt + 1} скачивания не удалась: {e}")
        await asyncio.sleep(2)

if not success:
    await message.reply("Не удалось скачать видео из-за сетевой ошибки. Попробуйте еще раз.")
    return

try:
    await message.answer("Скачано! Обрабатываю видео через moviepy...")
    
    # Обработка видео через moviepy
    clip = VideoFileClip(input_video_path)
    clip = clip.subclip(0, min(10, clip.duration))  # Обрезаем до 10 секунд
    
    target_height = 1920
    target_width = 1080
    clip = clip.resize(height=target_height)
    
    if clip.w > target_width:
        x_center = clip.w / 2
        clip = clip.crop(x1=x_center - target_width/2, y1=0, x2=x_center + target_width/2, y2=target_height)

    clip.write_videofile(output_video_path, fps=30, codec='libx264', audio_codec='aac', preset='ultrafast')
    clip.close()
    
    with open(output_video_path, 'rb') as video_file:
        await message.reply_video(video_file, caption="Готово! Твое видео смонтировано.")
        
except Exception as e:
    await message.reply(f"Произошла ошибка при монтаже: {e}")
    
finally:
    if os.path.exists(input_video_path):
        os.remove(input_video_path)
    if os.path.exists(output_video_path):
        os.remove(output_video_path)
async def main(): 
print("Бот запущен и ожидает видео...") 
await dp.start_polling(bot)

if name == 'main': 
try: 
asyncio.run(main()) 
except KeyboardInterrupt: 
print("Бот остановлен.")