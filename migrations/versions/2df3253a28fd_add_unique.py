"""add unique

Revision ID: 2df3253a28fd
Revises: 0b37ae7a3ce6
Create Date: 2023-07-25 13:17:47.777145

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = '2df3253a28fd'
down_revision = '0b37ae7a3ce6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'dish', ['title'])
    op.create_unique_constraint(None, 'menu', ['title'])
    op.create_unique_constraint(None, 'submenu', ['title'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'submenu', type_='unique')
    op.drop_constraint(None, 'menu', type_='unique')
    op.drop_constraint(None, 'dish', type_='unique')
    # ### end Alembic commands ###
