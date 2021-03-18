"""empty message

Revision ID: 450cfd8728e6
Revises: 
Create Date: 2021-03-15 23:18:49.136932

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '450cfd8728e6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Genres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('Genres_items',
    sa.Column('Venue_id', sa.Integer(), nullable=False),
    sa.Column('Genres_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['Genres_id'], ['Genres.id'], ),
    sa.ForeignKeyConstraint(['Venue_id'], ['Venue.id'], ),
    sa.PrimaryKeyConstraint('Venue_id', 'Genres_id')
    )
    op.alter_column('Venue', 'address',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Venue', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Venue', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('Venue', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    op.alter_column('Venue', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('Venue', 'state',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Venue', 'phone',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Venue', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('Venue', 'city',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.alter_column('Venue', 'address',
               existing_type=sa.VARCHAR(length=120),
               nullable=True)
    op.drop_table('Genres_items')
    op.drop_table('Genres')
    # ### end Alembic commands ###
