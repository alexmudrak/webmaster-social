from fastapi import APIRouter

router = APIRouter(
    prefix="/settings",
    tags=["Settings"],
)


@router.get(
    "/",
    summary="Get all settings from app.",
)
async def get_all_objects():
    return "Hello Settings!"
