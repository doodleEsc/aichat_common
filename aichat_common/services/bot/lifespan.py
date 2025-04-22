from fastapi import FastAPI

from aichat_common.db.dao.bot_dao import BotDAO
from aichat_common.services.bot.service import BotService


def init_bot_service(app: FastAPI) -> None:
    """
    Initialize and register the BotService instance to app.state.
    Should be called after DB and Redis are initialized.
    """
    bot_dao = BotDAO()
    # Redis pool is optional, pass if needed
    redis_pool = getattr(app.state, "redis_pool", None)
    app.state.bot_service = BotService(bot_dao=bot_dao, redis_pool=redis_pool)


async def shutdown_bot_service(app: FastAPI) -> None:
    """
    Shutdown logic for BotService, if any resource needs cleanup.
    """
    bot_service = getattr(app.state, "bot_service", None)
    if bot_service and hasattr(bot_service, "close"):
        await bot_service.close()
