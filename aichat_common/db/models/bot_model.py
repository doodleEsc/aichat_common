import pymongo
from typing import List
from pydantic import Field, BaseModel
from beanie import Document


class BotCloth(BaseModel):
    cloth_id: str = Field(..., description="服装的ID")
    cloth_description: str = Field(..., description="服装描述")
    cloth_in_use: bool = Field(default=False, description="服装是否正在使用")


class BotModel(Document):
    bot_id: str = Field(..., description="Client ID")
    bot_name: str = Field(...)
    bot_prop: str = Field(..., description="人物属性")
    bot_appearance: str = Field(..., description="人物外貌")
    bot_chat_rules: str = Field(..., description="聊天规则")
    bot_chat_topics: str = Field(..., description="聊天话题喜好")
    bot_personality: str = Field(..., description="人物性格")
    bot_ideal_match: str = Field(..., description="喜欢人的类型")
    bot_hobbies: str = Field(..., description="人物喜好")
    bot_food_likes: str = Field(..., description="食物偏好")
    bot_other_likes: str = Field(..., description="其他偏好")
    bot_special_skills: str = Field(..., description="特殊技能")
    bot_relationships: str = Field(..., description="角色关系")
    bot_character_background: str = Field(..., description="人物背景")
    bot_work_info: str = Field(..., description="工作信息")
    bot_clothes: List[BotCloth] = Field(default=[], description="衣物列表")

    class Settings:
        name = "bots"
        indexes = [
            pymongo.IndexModel([("bot_id", pymongo.ASCENDING)], unique=True),
        ]

    def __repr__(self) -> str:
        return f"<Bot({self.bot_name}) {self.bot_id}>"

    def __str__(self) -> str:
        return f"Bot: {self.bot_name} ({self.bot_id})"
