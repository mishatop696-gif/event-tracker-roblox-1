
import asyncio
import logging
from database import add_detection

logger = logging.getLogger(__name__)

CATEGORIES = [
    "Admin",
    "Video Star",
    "Developers",
    "Events"
]

class RobloxTracker:
    def __init__(self):
        self.running = False

    async def start(self):
        self.running = True
        logger.info("Roblox tracker started")

    async def stop(self):
        self.running = False
        logger.info("Roblox tracker stopped")

    async def check(self):
        if not self.running:
            return

        # Здесь будет подключение к проверенным
        # источникам данных Roblox.
        logger.info("Checking Roblox sources")

    async def run(self):
        await self.start()

        while self.running:
            try:
                await self.check()
            except Exception:
                logger.exception("Tracker error")

            await asyncio.sleep(60)

    def record_detection(
        self,
        category,
        username,
        event_name="",
        game_url=""
    ):
        if category not in CATEGORIES:
            raise ValueError("Unknown category")

        add_detection(
            category,
            username,
            event_name,
            game_url
        )
      
