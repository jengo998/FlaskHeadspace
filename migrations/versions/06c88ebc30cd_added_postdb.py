"""added PostDB

Revision ID: 06c88ebc30cd
Revises: b3a3d26760dc
Create Date: 2021-07-28 19:54:52.995528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06c88ebc30cd'
down_revision = 'b3a3d26760dc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('postDB',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('post', sa.String(length=2000), nullable=True),
    sa.Column('post_date', sa.String(length=32), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_postDB_post_date'), 'postDB', ['post_date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_postDB_post_date'), table_name='postDB')
    op.drop_table('postDB')
    # ### end Alembic commands ###
