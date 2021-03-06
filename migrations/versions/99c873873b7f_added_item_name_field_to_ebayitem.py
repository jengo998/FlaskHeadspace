"""Added item_name field to EbayItem

Revision ID: 99c873873b7f
Revises: 183493a890f2
Create Date: 2021-08-01 22:34:30.657066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99c873873b7f'
down_revision = '183493a890f2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ebay_item', sa.Column('item_name', sa.String(length=32), nullable=True))
    op.create_index(op.f('ix_ebay_item_item_name'), 'ebay_item', ['item_name'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ebay_item_item_name'), table_name='ebay_item')
    op.drop_column('ebay_item', 'item_name')
    # ### end Alembic commands ###
