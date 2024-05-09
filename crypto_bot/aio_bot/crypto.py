import asyncio
from telethon.sync import TelegramClient, events
from translatepy import Translator
import httpcore
#Акк с подпиской
translator = Translator()

api_id = '27182194'
api_hash = 'af5f7f0ac2df15eaa53f10b617deb96a'
phone_number = '+380507247808'

session_path = 'crypto_bot/sessions.session'
client = TelegramClient(session_path, api_id, api_hash)

@client.on(events.NewMessage)
async def handle_message(event):
    source_chat = -4231114720  # Откуда
    destination_chat = -1002020429767  # Куда (чат)

    if event.chat_id == source_chat:
        if event.message.photo:
            caption = event.message.text
            translated_caption = ""
            if caption:
                # Translate the text
                result = translator.translate(caption, "Russian")
                translated_caption = result.result
                print(translated_caption)
            # Forward the photo with the translated text
            await client.send_file(
                destination_chat,
                event.message.photo,
                caption=translated_caption
            )

        elif event.message.text:
            # Just text, translate and send
            result = translator.translate(event.message.text, "Russian")
            translated_text = result.result
            print(translated_text)
            await client.send_message(destination_chat, translated_text)

async def main():
    await client.start(phone_number)
    await client.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
