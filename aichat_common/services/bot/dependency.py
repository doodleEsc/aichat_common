from fastapi import Request
from aichat_common.services.bot.service import BotService


async def get_bot_service(request: Request) -> BotService:
    """
    FastAPI dependency to get the bot service instance.

    :param request: FastAPI request object.
    :return: BotService singleton instance.
    """
    return request.app.state.bot_service
