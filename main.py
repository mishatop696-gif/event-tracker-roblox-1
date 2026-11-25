
import os
import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from database import init_db, save_user, get_latest

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

router = Router()

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📊 Статус"),
            KeyboardButton(text="🎮 В событии")
        ],
        [
            KeyboardButton(text="🕒 Последние"),
            KeyboardButton(text="⚙️ Настройки")
        ],
        [
            KeyboardButton(text="🔵 Admin"),
            KeyboardButton(text="⭐ Video Star")
        ],
        [
            KeyboardButton(text="🛠️ Developers"),
            KeyboardButton(text="🔔 Уведомления")
        ]
    ],
    resize_keyboard=True
)


@router.message(CommandStart())
async def start(message: Message):
    init_db()
    save_user(message.from_user.id)

    await message.answer(
        "🌈 <b>Roblox Event Tracker</b>\n\n"
        "Добро пожаловать!\n"
        "Выбери раздел в меню.",
        reply_markup=menu
    )


@router.message(F.text == "📊 Статус")
async def status(message: Message):
    await message.answer(
        "📊 <b>Статус мониторинга</b>\n\n"
        "🔵 Admin: ожидает подключение\n"
        "⭐ Video Star: ожидает подключение\n"
        "🛠️ Developers: ожидает подключение\n"
        "🎮 Events: ожидает подключение"
    )


@router.message(F.text == "🕒 Последние")
async def latest(message: Message):
    records = get_latest(10)

    if not records:
        await message.answer(
            "🕒 <b>Последние обнаружения</b>\n\n"
            "Пока нет подтверждённых обнаружений."
        )
        return

    result = "🕒 <b>Последние обнаружения</b>\n\n"

    for category, username, event, url, date in records:
        result += (
            f"📌 {category}\n"
            f"👤 {username}\n"
            f"🎮 {event or 'Не указано'}\n"
            f"🕒 {date}\n"
            f"{url or ''}\n\n"
        )

    await message.answer(result)


@router.message(F.text == "🎮 В событии")
async def events(message: Message):
    await message.answer(
        "🎮 <b>Активные события</b>\n\n"
        "Источники мониторинга ещё подключаются."
    )


@router.message(F.text == "⚙️ Настройки")
async def settings(message: Message):
    await message.answer(
        "⚙️ <b>Настройки</b>\n\n"
        "Настройка категорий мониторинга скоро появится."
    )


@router.message(F.text == "🔵 Admin")
async def admin(message: Message):
    await message.answer("🔵 Мониторинг Roblox Admin готовится.")


@router.message(F.text == "⭐ Video Star")
async def video_star(message: Message):
    await message.answer("⭐ Мониторинг Video Star готовится.")


@router.message(F.text == "🛠️ Developers")
async def developers(message: Message):
    await message.answer("🛠️ Мониторинг разработчиков готовится.")


@router.message(F.text == "🔔 Уведомления")
async def notifications(message: Message):
    await message.answer("🔔 Настройки уведомлений готовятся.")


async def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is not configured")

    init_db()

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
        
