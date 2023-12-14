from sqlmodel import Field, SQLModel


class Projects(SQLModel, table=True):
    # type: ignore
    id: int = Field(default=None, nullable=False, primary_key=True)
