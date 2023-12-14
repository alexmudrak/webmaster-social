from fastapi import APIRouter

router = APIRouter(
    prefix="/dashboards",
    tags=["Dashboard"],
)


@router.get(
    "/",
    summary="Get all dashboard informations.",
)
async def get_all_objects():
    return "Hello Dashboard!"
