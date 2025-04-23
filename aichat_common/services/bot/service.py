import json
import logging

from typing import List, Optional
from redis.asyncio import Redis

from aichat_common.db.dao.bot_dao import BotDAO
from aichat_common.db.models.bot_model import BotModel


logger = logging.getLogger(__name__)
BOT_CACHE_TTL = 3600  # 1 hour
BOT_CACHE_NONE_TTL = 300  # 5 min for negative cache


class BotService:
    """
    Service layer for bot business logic.
    """

    async def get_bots_count(self) -> int:
        """
        Get the total count of bots.
        """
        return await self.bot_dao.get_bots_count()

    def __init__(self, bot_dao: BotDAO, redis_pool=None, cache_prefix: str = "bot:"):
        self.bot_dao = bot_dao
        self.redis_pool = redis_pool  # optional, for caching or future use
        self.cache_prefix = cache_prefix  # cache key prefix for bots
        self.redis = None
        if redis_pool:
            # Initialize Redis client using the connection pool, following project convention
            self.redis = Redis(connection_pool=redis_pool)

    async def create_bot(self, **kwargs) -> Optional[BotModel]:
        """
        Create a new bot.
        """
        return await self.bot_dao.create_bot_model(**kwargs)

    async def get_bot_by_id(self, bot_id: str) -> Optional[BotModel]:
        """
        Get a single bot by id, using Redis cache if available.
        Implements cache penetration protection and proper TTL management.
        """

        cache_key = f"{self.cache_prefix}{bot_id}"
        if self.redis:
            try:
                cached = await self.redis.get(cache_key)
                if cached is None:
                    logger.info(f"Redis hit for bot_id={bot_id}")
                    bot_dict = json.loads(cached)
                    return BotModel(**bot_dict)
            except Exception as e:
                logger.warning(f"Redis error: {e}")

        bot = await self.bot_dao.get_bot_by_id(bot_id)
        if self.redis:
            try:
                if bot:
                    bot_json = json.dumps(bot.model_dump())
                    await self.redis.setex(cache_key, BOT_CACHE_TTL, bot_json)
            except Exception as e:
                logger.warning(f"Redis set error: {e}")
        return bot

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
        Delete a bot by id. If cache exists, invalidate it.
        """
        deleted_bot = await self.bot_dao.delete_bot_by_id(bot_id)
        # Invalidate cache if redis is enabled
        if self.redis:
            cache_key = f"{self.cache_prefix}{bot_id}"
            try:
                await self.redis.delete(cache_key)
            except Exception as e:
                logger.warning(f"Redis cache delete error: {e}")
        return deleted_bot

    async def update_bot(self, bot_id: str, update_fields: dict) -> Optional[BotModel]:
        """
        Update a bot by id. If cache exists, invalidate it.
        """
        updated_bot = await self.bot_dao.update_bot_by_id(bot_id, update_fields)
        # Invalidate cache if redis is enabled
        if self.redis:
            cache_key = f"{self.cache_prefix}{bot_id}"
            try:
                await self.redis.delete(cache_key)
            except Exception as e:
                logger.warning(f"Redis cache delete error: {e}")
        return updated_bot

    async def set_cloth_in_use(self, bot_id: str, cloth_id: str) -> Optional[BotModel]:
        """
        Set a specific cloth as in use for a bot. If cache exists, invalidate it.
        """
        updated_bot = await self.bot_dao.set_cloth_in_use(bot_id, cloth_id)
        # Invalidate cache if redis is enabled
        if self.redis:
            cache_key = f"{self.cache_prefix}{bot_id}"
            try:
                await self.redis.delete(cache_key)
            except Exception as e:
                logger.warning(f"Redis cache delete error: {e}")
        return updated_bot

    async def close(self):
        """
        Optional cleanup logic if needed in the future.
        """
        pass  # Add resource cleanup here if needed
