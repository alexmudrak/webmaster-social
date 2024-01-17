"""feat: add try_count field to PublishArticleStatus model

Revision ID: 666e5e337a95
Revises: b98a625b6986
Create Date: 2023-12-25 15:40:45.287777

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "666e5e337a95"
down_revision: Union[str, None] = "b98a625b6986"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "publisharticlestatus",
        sa.Column(
            "try_count", sa.Integer(), nullable=False, server_default="0"
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("publisharticlestatus", "try_count")
    # ### end Alembic commands ###