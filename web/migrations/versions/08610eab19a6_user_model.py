"""User model.

Revision ID: 08610eab19a6
Revises:
Create Date: 2017-03-31 11:37:19.311485

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '08610eab19a6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=254), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('registered_at', sqlalchemy_utils.types.arrow.ArrowType(), nullable=True),
    sa.Column('last_seen', sqlalchemy_utils.types.arrow.ArrowType(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
