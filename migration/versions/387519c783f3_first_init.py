"""empty message

Revision ID: 387519c783f3
Revises:
Create Date: 2024-01-29 13:27:53.076922

"""
from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "387519c783f3"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "log_entry",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.Column("level", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "logger_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column(
            "message", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_log_entry_level"), "log_entry", ["level"], unique=False
    )
    op.create_index(
        op.f("ix_log_entry_logger_name"),
        "log_entry",
        ["logger_name"],
        unique=False,
    )
    op.create_index(
        op.f("ix_log_entry_message"), "log_entry", ["message"], unique=False
    )
    op.create_table(
        "project",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("url", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column(
            "parse_type", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column("parse_last_article_count", sa.Integer(), nullable=False),
        sa.Column("parse_article_url_element", sa.JSON(), nullable=True),
        sa.Column("parse_article_img_element", sa.JSON(), nullable=True),
        sa.Column("parse_article_body_element", sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", "url", name="unique_name_url"),
    )
    op.create_table(
        "article",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.Column("url", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("title", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column(
            "img_url", sqlmodel.sql.sqltypes.AutoString(), nullable=True
        ),
        sa.Column("body", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["project.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("project_id", "url", name="unique_project_url"),
    )
    op.create_table(
        "setting",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("settings", sa.JSON(), nullable=True),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["project.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "article_status",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("created", sa.DateTime(), nullable=False),
        sa.Column("updated", sa.DateTime(), nullable=False),
        sa.Column("article_id", sa.Integer(), nullable=False),
        sa.Column("setting_id", sa.Integer(), nullable=False),
        sa.Column(
            "status", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column(
            "status_text", sqlmodel.sql.sqltypes.AutoString(), nullable=True
        ),
        sa.Column("try_count", sa.Integer(), nullable=False),
        sa.Column("url", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.ForeignKeyConstraint(
            ["article_id"],
            ["article.id"],
        ),
        sa.ForeignKeyConstraint(
            ["setting_id"],
            ["setting.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "article_id", "setting_id", name="unique_article_setting"
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("article_status")
    op.drop_table("setting")
    op.drop_table("article")
    op.drop_table("project")
    op.drop_index(op.f("ix_log_entry_message"), table_name="log_entry")
    op.drop_index(op.f("ix_log_entry_logger_name"), table_name="log_entry")
    op.drop_index(op.f("ix_log_entry_level"), table_name="log_entry")
    op.drop_table("log_entry")
    # ### end Alembic commands ###
