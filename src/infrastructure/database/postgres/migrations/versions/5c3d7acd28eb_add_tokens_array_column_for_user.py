"""add tokens array column for user

Revision ID: 5c3d7acd28eb
Revises: 56532eec0f75
Create Date: 2024-02-11 12:44:32.558118

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5c3d7acd28eb"
down_revision: Union[str, None] = "56532eec0f75"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "user",
        sa.Column(
            "tokens",
            sa.ARRAY(sa.String(255)),
            nullable=False,
            server_default=r"{}",
        ),
    )


def downgrade() -> None:
    op.drop_column("user", "tokens")
