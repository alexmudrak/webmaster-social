from fastapi import APIRouter

router = APIRouter(
    prefix="/projects",
    tags=["Project"],
)


@router.get(
    "/",
    summary="Get all projects.",
)
async def get_all_objects():
    return "Hello Project!"
