from controllers.project_controller import ProjectController
from core.database import get_session
from fastapi import APIRouter, Depends, status
from models.project import Project
from schemas.project_schema import (
    ProjectCreate,
    ProjectRead,
    ProjectReadWithSettings,
    ProjectUpdate,
)
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(
    prefix="/projects",
    tags=["Project"],
)


@router.get(
    "/",
    summary="Get all projects",
    response_model=list[ProjectRead],
)
async def get_all_projects(
    session: AsyncSession = Depends(get_session),
):
    return await ProjectController(session).get_all_objects()


@router.get(
    "/{object_id}",
    summary="Get project by ID",
    response_model=ProjectReadWithSettings,
)
async def get_project_by_id(
    object_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await ProjectController(session).get_object(object_id)


@router.post(
    "/",
    summary="Create new project",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    object_data: ProjectCreate,
    session: AsyncSession = Depends(get_session),
):
    return await ProjectController(session).create_object(object_data)


@router.patch(
    "/{object_id}",
    summary="Update project by ID",
    response_model=Project,
)
async def update_project(
    object_id: int,
    object_data: ProjectUpdate,
    session: AsyncSession = Depends(get_session),
):
    return await ProjectController(session).update_object(
        object_id,
        object_data,
    )


@router.delete(
    "/{object_id}",
    summary="Delete project by ID",
)
async def delete_project(
    object_id: int,
    session: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    return await ProjectController(session).delete_object(object_id)
