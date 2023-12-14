from sqlmodel import Field, SQLModel


class DashboardData(SQLModel, table=True):
    # type: ignore
    __tablename__: str = "dashboard_data"

    id: int = Field(default=None, nullable=False, primary_key=True)
