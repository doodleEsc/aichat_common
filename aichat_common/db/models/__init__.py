"""aichat_common models."""

from typing import Sequence, Type

from beanie import Document

from aichat_common.db.models.bot_model import BotModel


def load_all_models() -> Sequence[Type[Document]]:
    """Load all models from this folder."""
    return [
        BotModel,
    ]
