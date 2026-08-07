"""leads outbox inbox

Revision ID: 521c26c7b1f9
Revises: 
Create Date: 2026-08-07 16:45:44.173315

"""
from typing import Sequence, Union

import sqlalchemy
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '521c26c7b1f9'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    op.execute("""
        CREATE TYPE lead_status AS ENUM (
            'new',
            'approved',
            'rejected'
        )
    """)

    op.create_table(
        "leads",
        sa.Column(
            "lead_id",
            sa.UUID(),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("phone", sa.Text(), nullable=False),
        sa.Column("source", sa.Text(), nullable=False),
        sa.Column("comment", sa.Text(), nullable=False),
        sa.Column(
            "status",
            sa.Text(),
            nullable=False,
            server_default="new",
        ),
    )


    op.create_table(
        "outbox",
        sa.Column(
            "event_id",
            sa.UUID(),
            primary_key=True,
            server_default=sa.text("uuid_generate_v4()"),
        ),
        sa.Column("event_type", sa.Text(), nullable=False),
        sa.Column("aggregate_id", sa.UUID(), nullable=True),
        sa.Column("occurred_at", sa.DateTime(), nullable=True),
        sa.Column("payload", sa.Text(), nullable=True),
        sa.Column(
            "status",
            sa.Text(),
            nullable=False,
            server_default="NEW",
        ),
    )

    # inbound_events
    op.create_table(
        "inbound_events",
        sa.Column(
            "event_id",
            sa.UUID(),
            primary_key=True,
        ),
        sa.Column(
            "occurred_at",
            sa.DateTime(),
            nullable=True,
        ),
    )


def downgrade():
    op.drop_table("inbound_events")
    op.drop_table("outbox")
    op.drop_table("leads")

    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp"')