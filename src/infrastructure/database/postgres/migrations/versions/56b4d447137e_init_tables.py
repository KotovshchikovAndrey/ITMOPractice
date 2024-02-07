"""init tables

Revision ID: 56b4d447137e
Revises: 
Create Date: 2024-02-07 03:35:03.667720

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "56b4d447137e"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "tag",
        sa.Column("name", sa.String(70), primary_key=True),
    )

    op.create_table(
        "city",
        sa.Column("pk", sa.UUID(), primary_key=True),
        sa.Column("name", sa.String(70), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("image_url", sa.String(255), nullable=True),
    )

    op.create_table(
        "point",
        sa.Column("pk", sa.UUID(), primary_key=True),
        sa.Column("title", sa.String(70), nullable=False),
        sa.Column("subtitle", sa.String(70), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("image_url", sa.String(255), nullable=True),
        sa.Column(
            "city_pk",
            sa.UUID(),
            sa.ForeignKey("city.pk", ondelete="CASCADE"),
            nullable=False,
        ),
    )

    op.create_table(
        "point_tag",
        sa.Column("pk", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "point_pk",
            sa.UUID(),
            sa.ForeignKey("point.pk", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "tag_name",
            sa.String(70),
            sa.ForeignKey("tag.name", ondelete="CASCADE"),
            nullable=False,
        ),
    )

    op.execute("""ALTER TABLE point ADD coordinates Point NOT NULL;""")

    op.execute(
        """CREATE UNIQUE INDEX ON point (cast(coordinates[0] as float), cast(coordinates[1] as float));"""
    )

    op.create_unique_constraint(
        constraint_name="point_tag_unique_constraint",
        table_name="point_tag",
        columns=["point_pk", "tag_name"],
    )


def downgrade() -> None:
    op.drop_table("point_tag")
    op.drop_table("point")
    op.drop_table("city")
    op.drop_table("tag")
