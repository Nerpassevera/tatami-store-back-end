"""Updates Address model

Revision ID: 475941200b24
Revises: ee21d1bddcf3
Create Date: 2025-02-09 01:19:34.175008

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '475941200b24'
down_revision = 'ee21d1bddcf3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('addresses', schema=None) as batch_op:
        batch_op.alter_column('latitude',
               existing_type=sa.VARCHAR(),
               type_=sa.Float(),
               existing_nullable=True)
        batch_op.alter_column('longitude',
               existing_type=sa.VARCHAR(),
               type_=sa.Float(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('addresses', schema=None) as batch_op:
        batch_op.alter_column('longitude',
               existing_type=sa.Float(),
               type_=sa.VARCHAR(),
               existing_nullable=True)
        batch_op.alter_column('latitude',
               existing_type=sa.Float(),
               type_=sa.VARCHAR(),
               existing_nullable=True)

    # ### end Alembic commands ###
