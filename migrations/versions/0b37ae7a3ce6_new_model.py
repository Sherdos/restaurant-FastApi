"""new model

Revision ID: 0b37ae7a3ce6
Revises:
Create Date: 2023-07-24 14:42:35.696680

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '0b37ae7a3ce6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menu',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('title', sa.String(length=30), nullable=True),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('submenu',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('title', sa.String(length=30), nullable=True),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('menu_id', sa.UUID(), nullable=True),
                    sa.ForeignKeyConstraint(['menu_id'], ['menu.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('dish',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('title', sa.String(length=30), nullable=True),
                    sa.Column('description', sa.String(), nullable=True),
                    sa.Column('price', sa.String(), nullable=True),
                    sa.Column('submenu_id', sa.UUID(), nullable=True),
                    sa.ForeignKeyConstraint(['submenu_id'], ['submenu.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dish')
    op.drop_table('submenu')
    op.drop_table('menu')
    # ### end Alembic commands ###
