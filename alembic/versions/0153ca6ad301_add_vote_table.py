"""add vote table

Revision ID: 0153ca6ad301
Revises: 58ed893779ca
Create Date: 2021-11-05 10:52:23.022723

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0153ca6ad301'
down_revision = '58ed893779ca'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )
    # ### end Alembic commands ###

    pass


def downgrade():
    pass
