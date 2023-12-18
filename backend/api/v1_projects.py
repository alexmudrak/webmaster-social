from datetime import datetime

from core.database import get_session
from fastapi import APIRouter, Depends, HTTPException
from models.project import Project, ProjectCreate, ProjectUpdate
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(
    prefix="/projects",
    tags=["Project"],
)


@router.get("/", summary="Get all projects", response_model=list[Project])
async def get_all_projects(session: AsyncSession = Depends(get_session)):
    query = select(Project)
    result = await session.execute(query)
    projects = result.scalars().all()
    return projects


@router.get(
    "/{project_id}", summary="Get project by ID", response_model=Project
)
async def get_project_by_id(
    project_id: int, session: AsyncSession = Depends(get_session)
):
    project = await session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", summary="Create new project", response_model=Project)
async def create_project(
    project_data: ProjectCreate, session: AsyncSession = Depends(get_session)
):
    if not project_data.url:
        raise HTTPException(status_code=400, detail="Invalid URL provided")

    existing_project = await session.execute(
        select(Project).where(
            (Project.name == project_data.name)
            & (Project.url == str(project_data.url))
        )
    )
    existing_project = existing_project.fetchone()

    if existing_project:
        raise HTTPException(
            status_code=409,
            detail=(
                "A project with the same name and "
                "URL combination already exists."
            ),
        )

    project = Project(
        name=project_data.name,
        url=str(project_data.url),
        active=project_data.active,
    )
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project


@router.patch(
    "/{project_id}", summary="Update project by ID", response_model=Project
)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    session: AsyncSession = Depends(get_session),
):
    if not project_data.url:
        raise HTTPException(status_code=400, detail="Invalid URL provided")

    project = await session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project.update(project_data.dict(exclude_unset=True))
    project.url = str(project_data.url)
    project.updated = datetime.utcnow()

    await session.commit()
    await session.refresh(project)
    return project


@router.delete("/{project_id}", summary="Delete project by ID")
async def delete_project(
    project_id: int, session: AsyncSession = Depends(get_session)
):
    project = await session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    await session.delete(project)
    await session.commit()
    return {"message": f"Project `{project_id}` was deleted"}
