from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, ConfigDict, field_validator


class BotClothDTO(BaseModel):
    """
    DTO for a single cloth item belonging to a bot.
    """

    cloth_id: str
    cloth_description: str
    cloth_in_use: bool = False


class BotDTO(BaseModel):
    """
    DTO for returning a bot's full information.
    """

    id: str
    bot_id: str
    bot_name: str
    bot_prop: str
    bot_appearance: str
    bot_chat_rules: str
    bot_chat_topics: str
    bot_personality: str
    bot_ideal_match: str
    bot_hobbies: str
    bot_food_likes: str
    bot_other_likes: str
    bot_special_skills: str
    bot_relationships: str
    bot_character_background: str
    bot_work_info: str
    bot_clothes: List[BotClothDTO] = []

    @field_validator("id", mode="before")
    @classmethod
    def parse_object_id(cls, v):
        return str(v)

    model_config = ConfigDict(from_attributes=True)


class BotCreateDTO(BaseModel):
    """
    DTO for creating a new bot.
    """

    bot_id: str
    bot_name: str
    bot_prop: str
    bot_appearance: str
    bot_chat_rules: str
    bot_chat_topics: str
    bot_personality: str
    bot_ideal_match: str
    bot_hobbies: str
    bot_food_likes: str
    bot_other_likes: str
    bot_special_skills: str
    bot_relationships: str
    bot_character_background: str
    bot_work_info: str
    bot_clothes: Optional[List[BotClothDTO]] = None


class BotUpdateDTO(BaseModel):
    """
    DTO for updating an existing bot. All fields optional.
    """

    bot_id: Optional[str] = None
    bot_name: Optional[str] = None
    bot_prop: Optional[str] = None
    bot_appearance: Optional[str] = None
    bot_chat_rules: Optional[str] = None
    bot_chat_topics: Optional[str] = None
    bot_personality: Optional[str] = None
    bot_ideal_match: Optional[str] = None
    bot_hobbies: Optional[str] = None
    bot_food_likes: Optional[str] = None
    bot_other_likes: Optional[str] = None
    bot_special_skills: Optional[str] = None
    bot_relationships: Optional[str] = None
    bot_character_background: Optional[str] = None
    bot_work_info: Optional[str] = None
    bot_clothes: Optional[List[BotClothDTO]] = None


class BotResponse(BaseModel):
    """
    Standard API response for a single bot.
    """

    data: BotDTO
    message: Optional[str] = "success"
    code: int = 0


class BotPageDataDTO(BaseModel):
    """
    DTO for paginated bot list data.
    """

    items: List[BotDTO]
    page: int
    size: int
    total: int
    total_pages: int


class BotPageResponse(BaseModel):
    """
    Standard API response for a paginated list of bots for web UI.
    """

    data: BotPageDataDTO
    message: Optional[str] = "success"
    code: int = 0


class SetClothInUseDTO(BaseModel):
    """
    DTO for setting a specific cloth as in use for a bot.
    """
    cloth_id: str

