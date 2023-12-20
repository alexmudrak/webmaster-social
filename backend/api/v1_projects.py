from controllers.project_controller import ProjectController
from core.database import get_session
from fastapi import APIRouter, Depends, status
from models.project import Project
from schemas.project_schema import (
    ProjectCreate,
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
    response_model=list[Project],
)
async def get_all_projects(
    session: AsyncSession = Depends(get_session),
):
    return await ProjectController(session).get_all_objects()


@router.get(
    "/{project_id}",
    summary="Get project by ID",
    response_model=ProjectReadWithSettings,
)
async def get_project_by_id(
    project_id: int,
    session: AsyncSession = Depends(get_session),
):
    return await ProjectController(session).get_object(project_id)


@router.post(
    "/",
    summary="Create new project",
    response_model=Project,
    status_code=status.HTTP_201_CREATED,
)
async def create_project(
    project_data: ProjectCreate,
    session: AsyncSession = Depends(get_session),
):
    return await ProjectController(session).create_object(project_data)


@router.patch(
    "/{project_id}",
    summary="Update project by ID",
    response_model=Project,
)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    session: AsyncSession = Depends(get_session),
):
    return await ProjectController(session).update_object(
        project_id,
        project_data,
    )


@router.delete(
    "/{project_id}",
    summary="Delete project by ID",
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_session),
) -> dict[str, str]:
    return await ProjectController(session).delete_object(project_id)
