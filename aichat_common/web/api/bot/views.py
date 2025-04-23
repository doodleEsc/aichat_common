from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, Path, status

from aichat_common.web.api.bot.schema import (
    BotDTO,
    BotCreateDTO,
    BotUpdateDTO,
    BotResponse,
    BotPageDataDTO,
    BotPageResponse,
    BotClothDTO,
    SetClothInUseDTO,
)
from aichat_common.services.bot.service import BotService
from aichat_common.services.bot.dependency import get_bot_service

router = APIRouter()


@router.get("/", response_model=BotPageResponse)
async def list_bots(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    bot_service: BotService = Depends(get_bot_service),
):
    """
    List all bots with pagination.
    """
    offset = (page - 1) * size
    bots = await bot_service.get_all_bots(limit=size, offset=offset)
    total = await bot_service.get_bots_count()  # Use actual count from DB
    total_pages = (total + size - 1) // size if size else 1
    items = [BotDTO.model_validate(bot, from_attributes=True) for bot in bots]
    data = BotPageDataDTO(
        items=items,
        page=page,
        size=size,
        total=total,
        total_pages=total_pages,
    )

    print(data.model_dump())

    return BotPageResponse(data=data)


@router.post("/", response_model=BotResponse, status_code=status.HTTP_201_CREATED)
async def create_bot(
    bot_in: BotCreateDTO,
    bot_service: BotService = Depends(get_bot_service),
):
    """
    Create a new bot.
    """
    bot = await bot_service.create_bot(**bot_in.model_dump())
    print(bot)

    if not bot:
        raise HTTPException(status_code=500, detail="create bot failed")

    # Usually, you would return the created object; here, just return a success response.
    return BotResponse(
        data=BotDTO(**bot.model_dump()),  # id should be set if returned by service
        message="Bot created successfully",
        code=0,
    )


@router.get("/{bot_id}", response_model=BotResponse)
async def get_bot(
    bot_id: str = Path(..., description="Bot ID"),
    bot_service: BotService = Depends(get_bot_service),
):
    """
    Get a single bot by ID.
    """
    bot = await bot_service.get_bot_by_id(bot_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    return BotResponse(data=BotDTO.model_validate(bot))


@router.patch("/{bot_id}", response_model=BotResponse)
async def update_bot(
    bot_id: str,
    bot_update: BotUpdateDTO,
    bot_service: BotService = Depends(get_bot_service),
):
    """
    Update a bot by ID.
    """
    update_fields = {k: v for k, v in bot_update.model_dump().items() if v is not None}
    if not update_fields:
        raise HTTPException(status_code=400, detail="No fields to update")
    updated_bot = await bot_service.update_bot(bot_id, update_fields)
    if not updated_bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    return BotResponse(data=BotDTO.model_validate(updated_bot))


@router.delete("/{bot_id}", response_model=BotResponse)
async def delete_bot(
    bot_id: str,
    bot_service: BotService = Depends(get_bot_service),
):
    """
    Delete a bot by ID.
    """
    deleted_bot = await bot_service.delete_bot(bot_id)
    if not deleted_bot:
        raise HTTPException(status_code=404, detail="Bot not found")
    return BotResponse(data=BotDTO.model_validate(deleted_bot), message="Bot deleted")


@router.post("/{bot_id}/clothes/use", response_model=BotResponse)
async def set_cloth_in_use(
    bot_id: str,
    params: SetClothInUseDTO,
    bot_service: BotService = Depends(get_bot_service),
):
    """
    Set a specific cloth as in use for a bot.
    """
    updated_bot = await bot_service.set_cloth_in_use(bot_id, params.cloth_id)
    if not updated_bot:
        raise HTTPException(status_code=404, detail="Bot or cloth not found")
    return BotResponse(
        data=BotDTO.model_validate(updated_bot, from_attributes=True),
        message="Cloth set in use",
    )
