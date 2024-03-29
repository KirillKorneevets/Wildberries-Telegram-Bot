"""empty message

Revision ID: 337e33d35ec8
Revises: 235132de1c2d
Create Date: 2024-03-12 16:08:11.517353

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '337e33d35ec8'
down_revision: Union[str, None] = '235132de1c2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('requests')
    op.add_column('users', sa.Column('article', sa.Integer(), nullable=True))
    op.add_column('users', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('subscribed', sa.Boolean(), nullable=True))
    op.create_unique_constraint(None, 'users', ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'subscribed')
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'article')
    op.create_table('requests',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('article', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('subscribed', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='requests_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='requests_pkey')
    )
    # ### end Alembic commands ###
