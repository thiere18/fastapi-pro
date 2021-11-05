"""add post teables

Revision ID: 938677b06b5a
Revises: 0153ca6ad301
Create Date: 2021-11-05 10:53:13.941981

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '938677b06b5a'
down_revision = '0153ca6ad301'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False,
                    primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')

    pass
