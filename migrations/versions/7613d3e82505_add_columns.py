"""add columns

Revision ID: 7613d3e82505
Revises: 055840b6af1e
Create Date: 2020-11-28 20:44:12.829420

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7613d3e82505'
down_revision = '055840b6af1e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hospitals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('area', sa.String(length=64), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_hospitals_name'), 'hospitals', ['name'], unique=False)
    op.create_table('chiryos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('hospital_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['hospital_id'], ['hospitals.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('kensas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('hospital_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['hospital_id'], ['hospitals.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('shikkans',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('hospital_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['hospital_id'], ['hospitals.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('opentimes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('from_time', sa.DateTime(), nullable=True),
    sa.Column('to_time', sa.DateTime(), nullable=True),
    sa.Column('kensa_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['kensa_id'], ['kensas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('opentimes')
    op.drop_table('shikkans')
    op.drop_table('kensas')
    op.drop_table('chiryos')
    op.drop_index(op.f('ix_hospitals_name'), table_name='hospitals')
    op.drop_table('hospitals')
    # ### end Alembic commands ###
