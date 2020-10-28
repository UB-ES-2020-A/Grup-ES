"""empty message

Revision ID: e6d30c3a6cf1
Revises: 
Create Date: 2020-10-28 13:01:50.803027

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6d30c3a6cf1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('books',
    sa.Column('isbn', sa.Integer(), nullable=False),
    sa.Column('vendible', sa.Boolean(), nullable=False),
    sa.Column('stock', sa.Integer(), nullable=False),
    sa.Column('precio', sa.Float(), nullable=False),
    sa.Column('titulo', sa.String(), nullable=False),
    sa.Column('autor', sa.String(), nullable=True),
    sa.Column('editorial', sa.String(), nullable=True),
    sa.Column('sinopsis', sa.String(), nullable=True),
    sa.Column('url_imagen', sa.String(), nullable=True),
    sa.Column('fecha_de_publicacion', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('isbn')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('role', sa.Enum('manager', 'user'), nullable=False),
    sa.Column('state', sa.Boolean(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('books')
    # ### end Alembic commands ###