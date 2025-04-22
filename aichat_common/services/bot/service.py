from typing import List, Optional

from aichat_common.db.dao.bot_dao import BotDAO
from aichat_common.db.models.bot_model import BotModel


class BotService:
    """
    Service layer for bot business logic.
    """

    def __init__(self, bot_dao: BotDAO, redis_pool=None):
        self.bot_dao = bot_dao
        self.redis_pool = redis_pool  # optional, for caching or future use

    async def create_bot(self, **kwargs) -> None:
        """
        Create a new bot.
        """
        await self.bot_dao.create_bot_model(**kwargs)

    async def get_all_bots(self, limit: int = 20, offset: int = 0) -> List[BotModel]:
        """
        Get all bots with pagination.
        """
        return await self.bot_dao.get_all_bots(limit, offset)

    async def get_bots(
        self, bot_id: Optional[str] = None, bot_name: Optional[str] = None
    ) -> List[BotModel]:
        """
        Filter bots by id or name.
        """
        return await self.bot_dao.filter(bot_id=bot_id, bot_name=bot_name)

    async def delete_bot(self, bot_id: str) -> Optional[BotModel]:
        """
        Delete a bot by id.
        """
        return await self.bot_dao.delete_bot_by_id(bot_id)

    async def update_bot(self, bot_id: str, update_fields: dict) -> Optional[BotModel]:
        """
        Update a bot by id.
        """
        return await self.bot_dao.update_bot_by_id(bot_id, update_fields)

    async def set_cloth_in_use(self, bot_id: str, cloth_id: str) -> Optional[BotModel]:
        """
        Set a specific cloth as in use for a bot.
        """
        return await self.bot_dao.set_cloth_in_use(bot_id, cloth_id)

    async def close(self):
        """
        Optional cleanup logic if needed in the future.
        """
        pass  # Add resource cleanup here if needed
