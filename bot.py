from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN, CHAT_ID

bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


async def send_notification(**data):
    text = f"<b>{data.get('title')}</b>\n\n" \
           f"{data.get('url')}"

    await dp.bot.send_message(
        chat_id=CHAT_ID,
        text=text
    )


if __name__ == '__main__':
    executor.start_polling(dp)
