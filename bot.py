import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.client.session.aiohttp import AiohttpSession
from aiohttp import ClientTimeout

API_TOKEN = "" 

FOOTER = (
    "\n\n"
    '<a href="your link">your text</a>\n'
    '<a href="your link">your text</a>'
)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

session = AiohttpSession(timeout=ClientTimeout(total=60, connect=30))
bot = Bot(token=API_TOKEN, session=session)
dp = Dispatcher()


@dp.channel_post()
async def on_channel_post(message: types.Message):
    log.info(f"got post")
    try:
        if message.text:
            new_text = message.text + FOOTER
            await bot.edit_message_text(
                text=new_text,
                chat_id=message.chat.id,
                message_id=message.message_id,
                parse_mode=ParseMode.HTML,
            )
            log.info("edited work")

        elif message.photo or message.video or message.audio or message.document or message.voice or message.video_note or message.animation:
            new_caption = (message.caption or "") + FOOTER
            await bot.edit_message_caption(
                chat_id=message.chat.id,
                message_id=message.message_id,
                caption=new_caption,
                parse_mode=ParseMode.HTML,
            )
            log.info("edited work")

    except Exception as e:
        log.error(f"failed to edit")


@dp.edited_channel_post()
async def on_edited_channel_post(message: types.Message):
    pass


async def main():
    log.info("starting")
    for attempt in range(5):
        try:
            await bot.delete_webhook(drop_pending_updates=True)
            break
        except Exception as e:
            log.warning(f"attempt delete")
            await asyncio.sleep(3)

    await dp.start_polling(bot, allowed_updates=["channel_post", "edited_channel_post"])


if __name__ == "__main__":
    asyncio.run(main())
