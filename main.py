
import os
import asyncio
import logging
import secrets
import hmac
from html import escape

from aiohttp import web

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    Update
)
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from database import init_db, save_user, get_latest
from members import get_members, get_all_members

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")
HOST = os.getenv("RENDER_EXTERNAL_HOSTNAME")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET") or secrets.token_urlsafe(32)

WEBHOOK_PATH = "/webhook"

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
        "Добро пожаловать!\n\n"
        "Выбери нужный раздел:",
        reply_markup=menu
    )


@router.message(F.text == "📊 Статус")
async def status(message: Message):
    counts = get_all_members()

    await message.answer(
        "📊 <b>Статус мониторинга</b>\n\n"
        f"🔵 Roblox Admin: {counts['admin']} аккаунтов\n"
        f"⭐ Video Star: {counts['video_star']} аккаунтов\n\n"
        "🛠️ Developers: отключены\n"
        "🎮 Мониторинг событий: готовится\n\n"
        "ℹ️ Автоматический сбор участников "
        "ещё не подключён."
    )


@router.message(F.text == "🔵 Admin")
async def admin(message: Message):
    members = get_members("admin")

    if not members:
        await message.answer(
            "🔵 <b>Roblox Admin</b>\n\n"
            "Список пока пуст.\n"
            "Аккаунты появятся после подключения "
            "доступных источников."
        )
        return

    result = "🔵 <b>Roblox Admin</b>\n\n"

    for member in members[:25]:
        username = escape(str(member["username"]))
        user_id = member["user_id"]

        result += (
            f"👤 @{username}\n"
            f"🆔 {user_id}\n\n"
        )

    await message.answer(result)


@router.message(F.text == "⭐ Video Star")
async def video_star(message: Message):
    members = get_members("video_star")

    if not members:
        await message.answer(
            "⭐ <b>Roblox Video Stars</b>\n\n"
            "Список пока пуст.\n"
            "Аккаунты появятся после подключения "
            "доступных источников."
        )
        return

    result = "⭐ <b>Roblox Video Stars</b>\n\n"

    for member in members[:25]:
        username = escape(str(member["username"]))
        user_id = member["user_id"]

        result += (
            f"👤 @{username}\n"
            f"🆔 {user_id}\n\n"
        )

    await message.answer(result)


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
            f"📌 {escape(str(category))}\n"
            f"👤 {escape(str(username))}\n"
            f"🎮 {escape(str(event or 'Не указано'))}\n"
            f"🕒 {escape(str(date))}\n\n"
        )

    await message.answer(result[:4000])


@router.message(F.text == "🎮 В событии")
async def events(message: Message):
    await message.answer(
        "🎮 <b>Roblox Events</b>\n\n"
        "Автоматическое обнаружение событий "
        "пока разрабатывается."
    )


@router.message(F.text == "⚙️ Настройки")
async def settings(message: Message):
    await message.answer(
        "⚙️ <b>Настройки</b>\n\n"
        "🔵 Roblox Admin — выбран\n"
        "⭐ Video Star — выбран\n"
        "🛠️ Developers — отключены\n\n"
        "Настройки уведомлений будут подключены "
        "следующим этапом."
    )


@router.message(F.text == "🔔 Уведомления")
async def notifications(message: Message):
    await message.answer(
        "🔔 <b>Уведомления</b>\n\n"
        "Система уведомлений пока готовится."
    )


async def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is not configured")

    if not HOST:
        raise RuntimeError(
            "RENDER_EXTERNAL_HOSTNAME is not configured"
        )

    init_db()

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )

    dp = Dispatcher()
    dp.include_router(router)

    async def health(request):
        return web.Response(text="Roblox Event Tracker is running")

    async def telegram_webhook(request):
        received_secret = request.headers.get(
            "X-Telegram-Bot-Api-Secret-Token", ""
        )

        if not hmac.compare_digest(
            received_secret, WEBHOOK_SECRET
        ):
            raise web.HTTPUnauthorized()

        try:
            data = await request.json()
            update = Update.model_validate(
                data,
                context={"bot": bot}
            )
            await dp.feed_update(bot, update)
        except Exception:
            logging.exception("Webhook update error")
            raise web.HTTPBadRequest()

        return web.Response(text="OK")

    app = web.Application()
    app.router.add_get("/", health)
    app.router.add_post(WEBHOOK_PATH, telegram_webhook)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.getenv("PORT", "10000"))
    site = web.TCPSite(runner, "0.0.0.0", port)

    try:
        await site.start()

        webhook_url = f"https://{HOST}{WEBHOOK_PATH}"

        await bot.set_webhook(
            url=webhook_url,
            secret_token=WEBHOOK_SECRET
        )

        logging.info("Roblox Event Tracker webhook started")

        await asyncio.Event().wait()

    finally:
        await runner.cleanup()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
    
