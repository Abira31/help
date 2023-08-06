"""empty message

Revision ID: b5447da0f13d
Revises: 1ce9c744f6d0
Create Date: 2022-08-01 16:40:43.088133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b5447da0f13d'
down_revision = '1ce9c744f6d0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('join_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'join_date')
    # ### end Alembic commands ###
