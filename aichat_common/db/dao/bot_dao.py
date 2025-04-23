from typing import List, Optional

from aichat_common.db.models.bot_model import BotModel, BotCloth


class BotDAO:
    """Class for accessing bot table."""

    async def get_bot_by_id(self, bot_id: str) -> Optional[BotModel]:
        """
        Get a single bot model by bot_id.

        :param bot_id: bot id.
        :return: BotModel instance or None if not found.
        """
        return await BotModel.find_one(BotModel.bot_id == bot_id)

    async def create_bot_model(self, **kwargs) -> None:
        """
        Add a single bot to the database.

        :param kwargs: fields for BotModel.
        """
        await BotModel.insert_one(BotModel(**kwargs))

    async def get_all_bots(self, limit: int, offset: int) -> List[BotModel]:
        """
        Get all bot models with limit/offset pagination.

        :param limit: limit of bots.
        :param offset: offset of bots.
        :return: list of bots.
        """
        return await BotModel.find_all(skip=offset, limit=limit).to_list()

    async def filter(
        self, bot_id: Optional[str] = None, bot_name: Optional[str] = None
    ) -> List[BotModel]:
        """
        Get specific bot models by bot_id or bot_name.

        :param bot_id: bot id.
        :param bot_name: bot name.
        :return: list of bots.
        """
        query = {}
        if bot_id is not None:
            query["bot_id"] = bot_id
        if bot_name is not None:
            query["bot_name"] = bot_name
        if not query:
            return []
        return await BotModel.find(query).to_list()

    async def delete_bot_by_id(self, bot_id: str) -> Optional[BotModel]:
        """
        Delete a bot model by bot_id.

        :param bot_id: bot id.
        :return: option of a bot model.
        """
        res = await BotModel.find_one(BotModel.bot_id == bot_id)
        if res is None:
            return res
        await res.delete()
        return res

    async def update_bot_by_id(
        self, bot_id: str, update_fields: dict
    ) -> Optional[BotModel]:
        """
        Update a bot model by bot_id.

        :param bot_id: bot id.
        :param update_fields: fields to update.
        :return: updated bot model or None.
        """
        bot = await BotModel.find_one(BotModel.bot_id == bot_id)
        if bot is None:
            return None
        for k, v in update_fields.items():
            setattr(bot, k, v)
        await bot.save()
        return bot

    async def set_cloth_in_use(self, bot_id: str, cloth_id: str) -> Optional[BotModel]:
        """
        Set a specific cloth as in use for a bot.

        :param bot_id: bot id.
        :param cloth_id: cloth id to set as in use.
        :return: updated bot model or None.
        """
        bot = await BotModel.find_one(BotModel.bot_id == bot_id)
        if bot is None:
            return None
        found = False
        for cloth in bot.bot_clothes:
            if cloth.cloth_id == cloth_id:
                cloth.cloth_in_use = True
                found = True
            else:
                cloth.cloth_in_use = False
        if not found:
            return None
        await bot.save()
        return bot
