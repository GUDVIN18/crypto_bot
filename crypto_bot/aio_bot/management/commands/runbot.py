# mybot/management/commands/runbot.py
from django.core.management.base import BaseCommand
from aio_bot.main_bot import main  # Импортируйте функцию main из вашего bot.py файла
from aio_bot.crypto import main as cr
import asyncio

class Command(BaseCommand):
    help = 'Запускает телеграм-бота'

    def handle(self, *args, **options):
        asyncio.run(main())

    # def crypto_py(self, *args, **options):
    #     asyncio.run(cr())
