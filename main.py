
import os
import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram import F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

router = Router()

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📊 Статус"),
         KeyboardButton(text="🎮 В событии")],
        [KeyboardButton(text="🕒 Последние"),
         KeyboardButton(text="⚙️ Настройки")],
        [KeyboardButton(text="🔵 Admin"),
         KeyboardButton(text="⭐ Video Star")],
        [KeyboardButton(text="🛠️ Developers"),
         KeyboardButton(text="🔔 Уведомления")]
    ],
    resize_keyboard=True
)

@router.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🌈 <b>Roblox Event Tracker</b>\n\n"
        "Добро пожаловать!\n"
        "Выбери нужный раздел в меню.",
        reply_markup=menu
    )

@router.message(F.text == "📊 Статус")
async def status(message: Message):
    await message.answer(
        "📊 <b>Статус мониторинга</b>\n\n"
        "🔵 Admin: подготовка\n"
        "⭐ Video Star: подготовка\n"
        "🛠️ Developers: подготовка\n"
        "🎮 Events: подготовка"
    )

@router.message(F.text == "🎮 В событии")
async def events(message: Message):
    await message.answer("🎮 Сейчас активные события проверяются.")

@router.message(F.text == "🕒 Последние")
async def latest(message: Message):
    await message.answer("🕒 История обнаружений пока пуста.")

@router.message(F.text == "⚙️ Настройки")
async def settings(message: Message):
    await message.answer("⚙️ Настройки уведомлений появятся здесь.")

@router.message(F.text == "🔵 Admin")
async def admin(message: Message):
    await message.answer("🔵 Раздел мониторинга Roblox Admin.")

@router.message(F.text == "⭐ Video Star")
async def video_star(message: Message):
    await message.answer("⭐ Раздел мониторинга Video Stars.")

@router.message(F.text == "🛠️ Developers")
async def developers(message: Message):
    await message.answer("🛠️ Раздел мониторинга разработчиков.")

@router.message(F.text == "🔔 Уведомления")
async def notifications(message: Message):
    await message.answer("🔔 Настройки уведомлений.")

async def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is not configured")

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
