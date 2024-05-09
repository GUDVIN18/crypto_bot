from pyrogram import Client, filters
import asyncio
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ChatMemberStatus
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import logging
from django.conf import settings
import re

#Акк без подписки

loop = asyncio.new_event_loop()
# channel_id = "-1002095000073"
channel_id = "-1002020429767"  # ID канала, откуда будут пересылаться сообщения
id_chanel_check = "-1002094896292"

API_TOKEN = settings.TELEGRAM_BOT_TOKEN
api_id = "21714885"   # Замените на ваш Telegram API ID
api_hash = "e94c81e6befbc9806cf68cdf8bbd6a40"  # Замените на ваш Telegram API Hash

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


from aio_bot import models
from .models import *
from datetime import timedelta
from django.utils import timezone
from asgiref.sync import sync_to_async

from django.utils.timezone import now, timedelta

@dp.callback_query_handler(lambda c: c.data == '24_hours')
async def handle_chat_message(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    try:
        user, created = await sync_to_async(BotUser.objects.get_or_create)(
            tg_id=user_id,
            defaults={
                'name': callback_query.from_user.first_name,  # Имя пользователя Telegram
                'subscription_end_date': now() + timedelta(days=1),  # Дата окончания подписки через 24 часа
                'is_trial': True,  # Установка флага пробного периода
                'is_paid': False  # Пометить, что пока оплата не произведена
            }
        )
        if created:
            await callback_query.message.edit_text(
                'Ваша бесплатная пробная версия активирована! Теперь сканер будет присылать вам интересные торговые '
                'возможности, вам не нужно ничего делать самостоятельно. Если вы хотите остановить оповещения, '
                'введите /stop.\nПо вопросам обращайтесь к @111. Желаем больших профитов!')
        else:
            await callback_query.message.edit_text(
                'Вы уже брали пробную подписку!\nПо вопросам обращайтесь к @111. Желаем больших профитов!')

    except Exception as e:
        await callback_query.message.reply_text('Произошла ошибка: {}'.format(str(e)))
        print(e)

        

# Определение синхронной функции для получения пользователей
def get_active_users():
    users_query = BotUser.objects.all().values_list('tg_id', flat=True)  # Получаем QuerySet
    return list(users_query)  # Преобразуем QuerySet в список


import cv2
import numpy as np

def photo_edit(photo_path):
    img = cv2.imread(photo_path)
    
    alpha = 1.3
    beta = -80
     # Получение размеров изображения
    height, width = img.shape[:2]

    # Обрезка снизу
    cropped_img = img[:height - 20]

    new_img = alpha * cropped_img + beta
    new_img = np.clip(new_img, 0, 255).astype(np.uint8)

    # Сохранение обработанного изображения
    cv2.imwrite(photo_path, new_img)
    print('Успех: изображение обработано и сохранено')




@dp.channel_post_handler(content_types=types.ContentType.ANY, chat_id=channel_id)
async def forward_message_to_users(message: types.Message):
    active_users_tg_ids = await sync_to_async(get_active_users)()  # Асинхронное получение списка активных пользователей

    # Обработка текста сообщения
    text = None
    if message.text or message.caption:
        original_text = message.text if message.text else message.caption
        text = re.sub(r'\b([A-Za-z]+usdt)]\b', lambda x: x.group(1).upper(), original_text)
        text = re.sub(r'\b([A-Za-z]+usdt)\b', lambda x: x.group(1).upper(), original_text)
        text = re.sub(r'\[Возьмите бонус на депозит в Bybit!\]', '', text)
        text = re.sub(r'\[20% скидка на ваши сборы в Bybit!\]', '', text)
        text = re.sub(r'\[?\]', '', text)
        text = re.sub(r'Следуйте за нами в Твиттере! \(https://twitter.com/100eyescrypto\)', '', text)
        text = re.sub(r'Бесплатный образовательный контент на нашем сайте', '', text)
        text = re.sub(r'20% Дополнительная скидка на ваши платы за сочетание! \(https://www.binance.com/en/register?ref=lkcug1at\)', '', text)
        text = re.sub(r'20% Дополнительная скидка на ваши платы за сочетание!', '', text)
        text = re.sub(r'\[\[\?', '', text)

        
        text = re.sub(r'\(https?://[^\)]*\)', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\s+', ' ', text).strip()
        
        print('text', text)

    # Обработка и отправка фото с текстом под ним
    if message.photo and text:
        photo = message.photo[-1]  # Берем самую большую версию фото
        file_info = await bot.get_file(photo.file_id)
        destination_path = f'media/{file_info.file_path.split("/")[-1]}'
        await bot.download_file(file_info.file_path, destination_path)

        # Редактирование фото и повторное сохранение по тому же пути
        photo_edit(destination_path)
        print(f"Файл сохранен в {destination_path}")


        # Пересылка фото с обработанным текстом капшена активным пользователям
        for tg_id in active_users_tg_ids:
            f = await sync_to_async(BotUser.objects.get)(tg_id=tg_id)
            if f.subscription_end_date < timezone.now():
                f.is_trial = False
                f.is_paid = False
                await sync_to_async(f.save)()

            
            if (f.is_trial is not False) or (f.is_paid is True):
                 with open(destination_path, 'rb') as photo_file:
                    await bot.send_photo(chat_id=tg_id, photo=photo_file, caption=text)
            else:
                print('Ошибка подписки при рассылке')



@dp.callback_query_handler(lambda c: c.data == 'bay_subscibe')
async def handle_chat_message(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    try:
        keyboard = types.InlineKeyboardMarkup()
        success_btn = types.InlineKeyboardButton(text="Подтвердить оплату", callback_data="verifications_pay")
        keyboard.add(success_btn)
        await callback_query.message.edit_text(f'''Стоимость подписки 20$.\nВыполните перевод на кошелек <b>TKfcvnzKRfYSczh9bg3xKeMFWs8gzACVDb</b> и пришлите скриншот в бота.\nПо вопросам обращайтесь к @111''', parse_mode='html',reply_markup=keyboard)
    except:
        print('Ошибка с подпиской')

        
@dp.callback_query_handler(lambda c: c.data == 'verifications_pay')
async def handle_chat_message(callback_query: types.CallbackQuery):
    try:
        await callback_query.message.edit_text(f'''Отправте скриншот перевода:''')
        await InputUserData.photo_user.set()
    except:
        print('Ошибка с подпиской')

from aiogram import types
from asgiref.sync import sync_to_async
from aiogram.dispatcher import FSMContext
from aiogram import types
from asgiref.sync import sync_to_async
from aiogram.dispatcher import FSMContext
from django.core.files.base import ContentFile
from .models import BayUsers, BotUser

import os
from aiogram import types
from aiogram.dispatcher import FSMContext
from asgiref.sync import sync_to_async
from django.core.files import File

@dp.message_handler(content_types=types.ContentType.PHOTO, state=InputUserData.photo_user)
async def handle_user_photo(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    bot_user = await sync_to_async(BotUser.objects.get)(tg_id=user_id)
    print(bot_user)
    photo = message.photo[-1]  # Берём последнюю (самую большую) версию фото

    file_info = await bot.get_file(photo.file_id)
    file = await bot.download_file(file_info.file_path)

    # Указываем путь для сохранения
    save_path = os.path.join('media/user_photos', f"{photo.file_id}.jpg")

    # Сохраняем файл
    with open(save_path, 'wb') as new_file:
        new_file.write(file.getvalue())

    # Создаем Django File объект для использования в ImageField
    django_file = File(open(save_path, 'rb'))

    try:
        bay_user, created = await sync_to_async(BayUsers.objects.update_or_create)(
            user=bot_user,
            defaults={'photo': django_file}
        )
        print("Запись в базу данных выполнена:", "создана" if created else "обновлена")
    except Exception as e:
        print("Ошибка при сохранении в базу данных:", str(e))

    django_file.close()  # Закрываем файл после использования

    print(f"Фото было сохранено по пути: {save_path}")
    await message.answer('Фотография успешно загружена!')
    await state.finish()








async def main():
    await dp.skip_updates()  # Пропускаем старые сообщения
    await dp.start_polling()

if __name__ == "__main__":
    loop.run_until_complete(main())