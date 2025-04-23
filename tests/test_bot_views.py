import uuid
import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status

from aichat_common.services.bot.service import BotService
from aichat_common.web.api.bot.schema import BotClothDTO
# from aichat_common.web.api.bot.schema import (
#     BotCreateDTO,
#     BotUpdateDTO,
#     SetClothInUseDTO,
# )


@pytest.mark.anyio
async def test_create_bot(
    fastapi_app: FastAPI, bot_service: BotService, client: AsyncClient
) -> None:
    """Test bot creation."""
    url = fastapi_app.url_path_for("create_bot")
    test_bot_id = uuid.uuid4().hex
    bot_data = {
        "bot_id": test_bot_id,
        "bot_name": "TestBot",
        "bot_prop": "test",
        "bot_appearance": "test",
        "bot_chat_rules": "rule",
        "bot_chat_topics": "topic",
        "bot_personality": "personality",
        "bot_ideal_match": "match",
        "bot_hobbies": "hobby",
        "bot_food_likes": "food",
        "bot_other_likes": "other",
        "bot_special_skills": "skills",
        "bot_relationships": "rel",
        "bot_character_background": "bg",
        "bot_work_info": "work",
        "bot_clothes": [],
    }

    response = await client.post(url, json=bot_data)
    assert response.status_code == status.HTTP_201_CREATED
    # Clean up
    await bot_service.delete_bot(test_bot_id)


@pytest.mark.anyio
async def test_get_bot(
    fastapi_app: FastAPI, bot_service: BotService, client: AsyncClient
) -> None:
    """Test bot retrieval."""
    test_bot_id = uuid.uuid4().hex
    bot_data = {
        "bot_id": test_bot_id,
        "bot_name": "TestBot",
        "bot_prop": "test",
        "bot_appearance": "test",
        "bot_chat_rules": "rule",
        "bot_chat_topics": "topic",
        "bot_personality": "personality",
        "bot_ideal_match": "match",
        "bot_hobbies": "hobby",
        "bot_food_likes": "food",
        "bot_other_likes": "other",
        "bot_special_skills": "skills",
        "bot_relationships": "rel",
        "bot_character_background": "bg",
        "bot_work_info": "work",
        "bot_clothes": [],
    }
    await bot_service.create_bot(**bot_data)
    url = fastapi_app.url_path_for("get_bot", bot_id=test_bot_id)
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["bot_id"] == test_bot_id
    # Clean up
    await bot_service.delete_bot(test_bot_id)


@pytest.mark.anyio
async def test_update_bot(
    fastapi_app: FastAPI, bot_service: BotService, client: AsyncClient
) -> None:
    """Test bot update."""
    test_bot_id = uuid.uuid4().hex
    bot_data = {
        "bot_id": test_bot_id,
        "bot_name": "TestBot",
        "bot_prop": "test",
        "bot_appearance": "test",
        "bot_chat_rules": "rule",
        "bot_chat_topics": "topic",
        "bot_personality": "personality",
        "bot_ideal_match": "match",
        "bot_hobbies": "hobby",
        "bot_food_likes": "food",
        "bot_other_likes": "other",
        "bot_special_skills": "skills",
        "bot_relationships": "rel",
        "bot_character_background": "bg",
        "bot_work_info": "work",
        "bot_clothes": [],
    }
    await bot_service.create_bot(**bot_data)
    url = fastapi_app.url_path_for("update_bot", bot_id=test_bot_id)
    patch_data = {"bot_name": "UpdatedBot"}
    response = await client.patch(url, json=patch_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["bot_name"] == "UpdatedBot"
    # Clean up
    await bot_service.delete_bot(test_bot_id)


@pytest.mark.anyio
async def test_delete_bot(
    fastapi_app: FastAPI, bot_service: BotService, client: AsyncClient
) -> None:
    """Test bot deletion."""
    test_bot_id = uuid.uuid4().hex
    bot_data = {
        "bot_id": test_bot_id,
        "bot_name": "TestBot",
        "bot_prop": "test",
        "bot_appearance": "test",
        "bot_chat_rules": "rule",
        "bot_chat_topics": "topic",
        "bot_personality": "personality",
        "bot_ideal_match": "match",
        "bot_hobbies": "hobby",
        "bot_food_likes": "food",
        "bot_other_likes": "other",
        "bot_special_skills": "skills",
        "bot_relationships": "rel",
        "bot_character_background": "bg",
        "bot_work_info": "work",
        "bot_clothes": [],
    }
    await bot_service.create_bot(**bot_data)
    url = fastapi_app.url_path_for("delete_bot", bot_id=test_bot_id)
    response = await client.delete(url)
    assert response.status_code == status.HTTP_200_OK
    # Ensure deleted
    get_url = fastapi_app.url_path_for("get_bot", bot_id=test_bot_id)
    response2 = await client.get(get_url)
    assert response2.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_list_bots(
    fastapi_app: FastAPI, bot_service: BotService, client: AsyncClient
) -> None:
    """Test bot list API."""
    test_bot_id = uuid.uuid4().hex
    bot_data = {
        "bot_id": test_bot_id,
        "bot_name": "TestBot",
        "bot_prop": "test",
        "bot_appearance": "test",
        "bot_chat_rules": "rule",
        "bot_chat_topics": "topic",
        "bot_personality": "personality",
        "bot_ideal_match": "match",
        "bot_hobbies": "hobby",
        "bot_food_likes": "food",
        "bot_other_likes": "other",
        "bot_special_skills": "skills",
        "bot_relationships": "rel",
        "bot_character_background": "bg",
        "bot_work_info": "work",
        "bot_clothes": [],
    }
    await bot_service.create_bot(**bot_data)
    url = fastapi_app.url_path_for("list_bots")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    items = response.json()["data"]["items"]
    assert any(item["bot_id"] == test_bot_id for item in items)
    # Clean up
    await bot_service.delete_bot(test_bot_id)


@pytest.mark.anyio
async def test_set_cloth_in_use(
    fastapi_app: FastAPI, bot_service: BotService, client: AsyncClient
) -> None:
    """Test setting a cloth in use for a bot."""
    test_bot_id = uuid.uuid4().hex
    # cloth = BotClothDTO(cloth_id="c1", cloth_description="desc", cloth_in_use=False)
    bot_data = {
        "bot_id": test_bot_id,
        "bot_name": "TestBot",
        "bot_prop": "test",
        "bot_appearance": "test",
        "bot_chat_rules": "rule",
        "bot_chat_topics": "topic",
        "bot_personality": "personality",
        "bot_ideal_match": "match",
        "bot_hobbies": "hobby",
        "bot_food_likes": "food",
        "bot_other_likes": "other",
        "bot_special_skills": "skills",
        "bot_relationships": "rel",
        "bot_character_background": "bg",
        "bot_work_info": "work",
        "bot_clothes": [
            {"cloth_id": "c1", "cloth_description": "desc", "cloth_in_use": False}
        ],
    }
    await bot_service.create_bot(**bot_data)
    url = fastapi_app.url_path_for("set_cloth_in_use", bot_id=test_bot_id)
    response = await client.post(url, json={"cloth_id": "c1"})
    assert response.status_code == status.HTTP_200_OK
    clothes = response.json()["data"]["bot_clothes"]
    assert any(cloth["cloth_id"] == "c1" and cloth["cloth_in_use"] for cloth in clothes)
    # Clean up
    await bot_service.delete_bot(test_bot_id)
