"""create user tables

Revision ID: 56532eec0f75
Revises: 56b4d447137e
Create Date: 2024-02-07 23:06:01.793124

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "56532eec0f75"
down_revision: Union[str, None] = "56b4d447137e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("pk", sa.UUID(), primary_key=True),
        sa.Column("name", sa.String(70), nullable=False),
        sa.Column("surname", sa.String(70), nullable=False),
        sa.Column("email", sa.String(70), nullable=False, unique=True),
        sa.Column("birthday", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=False), nullable=False),
    )

    op.create_table(
        "favorite_point",
        sa.Column("pk", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "user_pk",
            sa.UUID(),
            sa.ForeignKey("user.pk", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "point_pk",
            sa.UUID(),
            sa.ForeignKey("point.pk", ondelete="CASCADE"),
            nullable=False,
        ),
    )

    op.create_unique_constraint(
        constraint_name="user_favirite_point_unique_constraint",
        table_name="favorite_point",
        columns=["user_pk", "point_pk"],
    )


def downgrade() -> None:
    op.drop_table("favorite_point")
    op.drop_table("user")
