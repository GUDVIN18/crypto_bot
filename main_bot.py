from pyrogram import Client, filters
import asyncio
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ChatMemberStatus
import re

api_id = "22978582"   # Замените на ваш Telegram API ID
api_hash = "4015fe11039e83f88949ffbb62b5c252"  # Замените на ваш Telegram API Hash
bot_token = "6768058874:AAGUOb0Va_1CQ6Z9G84aVfj3yYW6Gw3bbQM"  # Токен вашего бота, полученный от BotFather

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

channel_id = "-1001234567890"  # ID канала, откуда будут пересылаться сообщения

id_chanel_check = ""

API_TOKEN = "6768058874:AAGUOb0Va_1CQ6Z9G84aVfj3yYW6Gw3bbQM" 
api_id = "22978582"   # Замените на ваш Telegram API ID
api_hash = "4015fe11039e83f88949ffbb62b5c252"  # Замените на ваш Telegram API Hash
channel_id = "-1002020429767"
  # Список ID пользователей, которым будут пересылаться сообщения

user_ids = set()  # Используем множество для хранения уникальных ID пользователей

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.channel_post_handler(content_types=types.ContentType.ANY, chat_id=channel_id)
async def forward_message_to_users(message: types.Message):
    for user_id in user_ids:
        a = message.send_copy(chat_id=user_id)
        print(message.text)
        await a

@dp.message_handler(commands=['start'])
async def register_user(message: types.Message):
    user_id = message.from_user.id
    channel_username = '@crypto_channel_test0000'  # Замените на username вашего канала
    try:
        user_channel_status = await bot.get_chat_member(chat_id=channel_username, user_id=message.from_user.id)
        if user_channel_status.status not in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
            await message.answer("Вы подписаны на канал!")
        else:
            await message.answer("Вы не подписаны на канал.")
    except Exception as e:
        await message.answer("Произошла ошибка при проверке подписки.")
        print(e)  # Логируем ошибку для отладки
    print(user_channel_status)
    if user_id not in user_ids:
        user_ids.add(user_id)
        await message.reply("Вы успешно подписаны на рассылку сообщений из канала!")
    else:
        await message.reply("Вы уже подписаны.")

async def main():
    await dp.skip_updates()  # Пропускаем старые сообщения
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())