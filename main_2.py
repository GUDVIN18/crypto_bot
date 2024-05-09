from pyrogram import Client, filters
import asyncio
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ChatMemberStatus
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
import re
channel_id = "-1001234567890"  # ID канала, откуда будут пересылаться сообщения

id_chanel_check = "-1002094896292"

API_TOKEN = "6768058874:AAGUOb0Va_1CQ6Z9G84aVfj3yYW6Gw3bbQM" 
api_id = "22978582"   # Замените на ваш Telegram API ID
api_hash = "4015fe11039e83f88949ffbb62b5c252"  # Замените на ваш Telegram API Hash
channel_id = "-1002020429767"
  # Список ID пользователей, которым будут пересылаться сообщения
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=API_TOKEN)

user_ids = set()  # Используем множество для хранения уникальных ID пользователей

bot = Bot(token=API_TOKEN)
# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize FSM storage
memory_storage = MemoryStorage()
dp = Dispatcher(bot, storage=memory_storage)

class InputUserData(StatesGroup):
    photo_user = State()


active_users = set()

@dp.message_handler(commands=['start'])
async def register_user(message: types.Message):
    user_channel_status = await bot.get_chat_member(chat_id=id_chanel_check, user_id=message.chat.id)
    user_channel_status = re.findall(r"\w*", str(user_channel_status))

    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Подписаться на канал", url="https://t.me/crypto_channel_test0000")
    success_btn = types.InlineKeyboardButton(text="Готово!", callback_data="check_subscription")
    keyboard.add(url_button, success_btn)
    await bot.send_message(message.chat.id, 'Отлично! Для начала подпишитесь на канал.', reply_markup=keyboard)



@dp.message_handler(commands=['stop'])
async def stop_subscription(message: types.Message):
    user_id = message.from_user.id
    if user_id in active_users:
        active_users.remove(user_id)
        await message.answer("Вы успешно отписались от рассылки.")
    else:
        await message.answer("Вы и не были подписаны.")



@dp.callback_query_handler(lambda c: c.data == 'check_subscription')
async def handle_chat_message(callback_query: types.CallbackQuery):
    channel_username = '@crypto_channel_test0000'  # Замените на ваш username канала
    user_id = callback_query.from_user.id
    try:
        user_channel_status = await bot.get_chat_member(chat_id=channel_username, user_id=user_id)
        if user_channel_status.status not in [ChatMemberStatus.LEFT, ChatMemberStatus.KICKED]:
            response_text = 'Успешно! Выберите подписку'

            keyboard = types.InlineKeyboardMarkup()
            url_button = types.InlineKeyboardButton(text="Пробный период 24ч", callback_data="24_hours")
            success_btn = types.InlineKeyboardButton(text="Купить подписку", callback_data="bay_subscibe")
            keyboard.add(url_button, success_btn)
            await callback_query.message.edit_text(f'<b>{response_text}</b>', parse_mode='html', reply_markup=keyboard)

        else:
            response_text = 'Подпишитесь на канал!'
            keyboard = types.InlineKeyboardMarkup()
            url_button = types.InlineKeyboardButton(text="Подписаться на канал", url="https://t.me/crypto_channel_test0000")
            success_btn = types.InlineKeyboardButton(text="Готово!", callback_data="check_subscription")
            keyboard.add(url_button, success_btn)
            await callback_query.message.edit_text(f'<b>{response_text}</b>', parse_mode='html', reply_markup=keyboard)

    except Exception as e:
        print(f"Ошибка: {e}")
        response_text = 'Произошла ошибка при проверке подписки.'
        keyboard = types.InlineKeyboardMarkup()
        url_button = types.InlineKeyboardButton(text="Подписаться на канал", url="https://t.me/crypto_channel_test0000")
        success_btn = types.InlineKeyboardButton(text="Готово!", callback_data="check_subscription")
        keyboard.add(url_button, success_btn)
        await callback_query.message.edit_text(f'<b>{response_text}</b>', parse_mode='html', reply_markup=keyboard)
    await callback_query.answer()



@dp.callback_query_handler(lambda c: c.data == '24_hours')
async def handle_chat_message(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    try:
        active_users.add(user_id)
        await callback_query.message.edit_text(f'''Ваша бесплатная пробная версия активирована! Теперь сканер будет присылать вам интересные торговые возможности, вам не нужно ничего делать самостоятельно. Если вы хотите остановить оповещения, введите /stop.
                                                По вопросам обращайтесь к @111. Желаем больших профитов!''')
    except Exception as e:
        print(e)



@dp.channel_post_handler(content_types=types.ContentType.ANY, chat_id=channel_id)
async def forward_message_to_users(message: types.Message):
    # Проверка и вывод текста сообщения, если он есть
    if message.text:
        print("Текст сообщения:", message.text)

    # Проверка и вывод информации о фото, если оно есть
    if message.photo:
        photo = message.photo[-1]  # Берем самую большую версию фото
        print("ID фото:", photo.file_id)
        print("Размеры фото:", photo.width, "x", photo.height)
        
    if message.caption:
            print("Подпись к фото:", message.caption)

    # Пересылка сообщения активным пользователям
    for user_id in active_users:
        await message.send_copy(chat_id=user_id)



@dp.callback_query_handler(lambda c: c.data == 'bay_subscibe')
async def handle_chat_message(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    try:
        keyboard = types.InlineKeyboardMarkup()
        success_btn = types.InlineKeyboardButton(text="Подтвердить оплату", callback_data="verifications_pay")
        keyboard.add(success_btn)
        await callback_query.message.edit_text(f'''Стоимость подписки 20$.\nВыполните перевод на кошелек и пришлите скриншот в бота.\nПо вопросам обращайтесь к @111''', reply_markup=keyboard)
    except:
        print('Ошибка с подпиской')

        
@dp.callback_query_handler(lambda c: c.data == 'verifications_pay')
async def handle_chat_message(callback_query: types.CallbackQuery):
    try:
        await callback_query.message.edit_text(f'''Отправте скриншот перевода:''')
        await InputUserData.photo_user.set()
    except:
        print('Ошибка с подпиской')


@dp.message_handler(content_types=types.ContentType.PHOTO, state=InputUserData.photo_user)
async def handle_user_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id  # Получаем ID последнего (самого большого) фото
    if photo_id is not None:
        await bot.send_message(message.chat.id, 'Успешно! Ожидайте, после проверки менеджер с Вами свяжется')
    await state.finish()







async def main():
    await dp.skip_updates()  # Пропускаем старые сообщения
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())