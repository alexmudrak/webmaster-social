from controllers.dashboard_controller import DashboardController
from core.database import get_session_context
from fastapi import APIRouter, Depends
from schemas.dashboard_schema import DashboardCardData, DashboardStatusesData
from sqlmodel.ext.asyncio.session import AsyncSession

router = APIRouter(
    prefix="/dashboards",
    tags=["Dashboard"],
)


@router.get(
    "/cards",
    summary="Get data for cards.",
    response_model=DashboardCardData,
)
async def get_cards_data(
    db_manager: AsyncSession = Depends(get_session_context),
):
    return await DashboardController(db_manager).get_cards_data()


@router.get(
    "/statuses",
    summary="Get data for statuses.",
    response_model=list[DashboardStatusesData],
)
async def get_statuses_data(
    db_manager: AsyncSession = Depends(get_session_context),
):
    return await DashboardController(db_manager).get_statuses_data()
