from controllers.setting_controller import SettingController
from core.database import get_session
from fastapi import APIRouter, Depends, status
from schemas.setting_schema import (
    SettingCreate,
    SettingRead,
    SettingReadWithProject,
    SettingUpdate,
)
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)


@router.get(
    "/",
    summary="Get all settings",
    response_model=list[SettingRead],
)
async def get_all_settings(
    session: AsyncSession = Depends(get_session),
):
    return SettingController(session).get_all_objects()


@router.get(
    "/{setting_id}",
    summary="Get setting by ID",
    response_model=SettingReadWithProject,
)
async def get_object_by_id(
    object_id: int,
    session: AsyncSession = Depends(get_session),
):
    return SettingController(session).get_object(object_id)


@router.post(
    "/",
    summary="Create new setting",
    response_model=SettingRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_object(
    object_data: SettingCreate,
    session: AsyncSession = Depends(get_session),
):
    return SettingController(session).create_object(object_data)


@router.patch(
    "/{project_id}",
    summary="Update setting by ID",
    response_model=SettingRead,
)
async def update_object(
    object_id: int,
    object_data: SettingUpdate,
    session: AsyncSession = Depends(get_session),
):
    return SettingController(session).update_object(object_id, object_data)


@router.delete(
    "/{setting_id}",
    summary="Delete setting by ID",
)
async def delete_object(
    object_id: int,
    session: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    return SettingController(session).delete_object(object_id)
