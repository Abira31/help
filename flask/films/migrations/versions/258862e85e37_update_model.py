"""update model

Revision ID: 258862e85e37
Revises: 2ecc72d106fd
Create Date: 2023-04-17 15:39:42.082465

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '258862e85e37'
down_revision = '2ecc72d106fd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('actors')
    # ### end Alembic commands ###
