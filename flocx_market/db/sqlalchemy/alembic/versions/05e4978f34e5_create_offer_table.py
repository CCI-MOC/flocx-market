"""Create offer table

Revision ID: 05e4978f34e5
Revises: 
Create Date: 2019-06-17 14:03:03.041180

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer, String, DateTime, Enum
import enum
import datetime
import sqlalchemy_jsonfield

# revision identifiers, used by Alembic.
revision = '05e4978f34e5'
down_revision = None
branch_labels = None
depends_on = None

class statusEnum(enum.Enum):
    available = 1
    matched = 2
    used = 3
    cancelled = 4
    expired = 5

def upgrade():
    op.create_table(
        'offer',
        sa.Column('id',Integer, primary_key=True, autoincrement=True),
        sa.Column('marketplace_offer_id',String(64), nullable=False, unique=True),
        sa.Column('provider_id', String(64), nullable=False, unique=True),
        sa.Column('creator_id', String(64), nullable=False, unique=True),
        sa.Column('marketplace_date_created',DateTime(timezone=True), nullable=False),
        sa.Column('status',String(15), nullable=False, default = 'available'),
        sa.Column('server_name',String(64), nullable=False, unique=True),
        sa.Column('start_time', DateTime(timezone=True), nullable=False),
        sa.Column('end_time',DateTime(timezone=True), nullable=False),
        sa.Column('duration',Integer, nullable=False),
        sa.Column('server_config',sqlalchemy_jsonfield.JSONField(
            # MariaDB does not support JSON for now
            enforce_string=True,
            # MariaDB connector requires additional parameters for correct UTF-8
            enforce_unicode=False
        ),
        nullable=False),
         sa.Column('cost',Integer, nullable=False)

    )



def downgrade():
    op.drop_table('offer')
