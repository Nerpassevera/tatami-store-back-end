"""User uses cognito_id as ID

Revision ID: 17e1e07ba649
Revises: cd679b6ab57b
Create Date: 2025-02-01 17:05:15.251661

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '17e1e07ba649'
down_revision = 'cd679b6ab57b'
branch_labels = None
depends_on = None


def upgrade():
    # Drop foreign key constraints
    op.drop_constraint("addresses_user_id_fkey", "addresses", type_="foreignkey")
    op.drop_constraint("carts_user_id_fkey", "carts", type_="foreignkey")
    op.drop_constraint("orders_user_id_fkey", "orders", type_="foreignkey")

    # Change user_id and id column types
    with op.batch_alter_table('addresses', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.dialects.postgresql.UUID(),
               type_=sa.String(),
               existing_nullable=False)

    with op.batch_alter_table('carts', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.dialects.postgresql.UUID(),
               type_=sa.String(),
               existing_nullable=False)

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.dialects.postgresql.UUID(),
               type_=sa.String(),
               existing_nullable=False)

    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.dialects.postgresql.UUID(),
               type_=sa.String(),
               existing_nullable=False)

    # Recreate foreign key constraints with the correct type
    op.create_foreign_key(
        "addresses_user_id_fkey",
        "addresses",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE"
    )

    op.create_foreign_key(
        "carts_user_id_fkey",
        "carts",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE"
    )

    op.create_foreign_key(
        "orders_user_id_fkey",
        "orders",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE"
    )


def downgrade():
    # Drop foreign key constraints
    op.drop_constraint("addresses_user_id_fkey", "addresses", type_="foreignkey")
    op.drop_constraint("carts_user_id_fkey", "carts", type_="foreignkey")
    op.drop_constraint("orders_user_id_fkey", "orders", type_="foreignkey")

    # Revert column type changes
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.String(),
               type_=sa.dialects.postgresql.UUID(),
               existing_nullable=False)

    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.String(),
               type_=sa.dialects.postgresql.UUID(),
               existing_nullable=False)

    with op.batch_alter_table('carts', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.String(),
               type_=sa.dialects.postgresql.UUID(),
               existing_nullable=False)

    with op.batch_alter_table('addresses', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.String(),
               type_=sa.dialects.postgresql.UUID(),
               existing_nullable=False)

    # Recreate original foreign key constraints
    op.create_foreign_key(
        "addresses_user_id_fkey",
        "addresses",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE"
    )

    op.create_foreign_key(
        "carts_user_id_fkey",
        "carts",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE"
    )

    op.create_foreign_key(
        "orders_user_id_fkey",
        "orders",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE"
    )