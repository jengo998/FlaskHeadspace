"""added mean and median fields to EbayItem

Revision ID: 0b8842ba0cae
Revises: c427e4a898b0
Create Date: 2021-08-02 01:51:59.148116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0b8842ba0cae'
down_revision = 'c427e4a898b0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ebay_item', sa.Column('mean', sa.Float(), nullable=True))
    op.add_column('ebay_item', sa.Column('median', sa.Float(), nullable=True))
    op.create_index(op.f('ix_ebay_item_mean'), 'ebay_item', ['mean'], unique=False)
    op.create_index(op.f('ix_ebay_item_median'), 'ebay_item', ['median'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ebay_item_median'), table_name='ebay_item')
    op.drop_index(op.f('ix_ebay_item_mean'), table_name='ebay_item')
    op.drop_column('ebay_item', 'median')
    op.drop_column('ebay_item', 'mean')
    # ### end Alembic commands ###
