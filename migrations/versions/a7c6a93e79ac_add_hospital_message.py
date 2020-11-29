"""add hospital message

Revision ID: a7c6a93e79ac
Revises: f4561d1a8970
Create Date: 2020-11-29 11:20:25.458405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7c6a93e79ac'
down_revision = 'f4561d1a8970'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('from_hospital_id', sa.Integer(), nullable=False),
    sa.Column('to_hospital_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['from_hospital_id'], ['hospitals.id'], ),
    sa.ForeignKeyConstraint(['to_hospital_id'], ['hospitals.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    # ### end Alembic commands ###
