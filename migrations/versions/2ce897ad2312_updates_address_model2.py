"""Updates Address model2

Revision ID: 2ce897ad2312
Revises: 475941200b24
Create Date: 2025-02-09 01:36:04.873834

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ce897ad2312'
down_revision = '475941200b24'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('addresses', schema=None) as batch_op:
        batch_op.add_column(sa.Column('unit', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('addresses', schema=None) as batch_op:
        batch_op.drop_column('unit')

    # ### end Alembic commands ###
