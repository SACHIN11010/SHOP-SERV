"""Add reviews table

Revision ID: 20241110_add_reviews_table
Revises: 20241110_add_shop_location_fields
Create Date: 2024-11-10 21:35:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '20241110_add_reviews_table'
down_revision = '20241110_add_shop_location_fields'
branch_labels = None
depends_on = None

def upgrade():
    # Create reviews table
    op.create_table('reviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('shop_id', sa.Integer(), nullable=True),
        sa.Column('product_id', sa.Integer(), nullable=True),
        sa.Column('rating', sa.Integer(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['shop_id'], ['shops.id'], ),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add rating columns to shops and products
    with op.batch_alter_table('shops', schema=None) as batch_op:
        batch_op.add_column(sa.Column('average_rating', sa.Float(), default=0.0))
        batch_op.add_column(sa.Column('review_count', sa.Integer(), default=0))
    
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('average_rating', sa.Float(), default=0.0))
        batch_op.add_column(sa.Column('review_count', sa.Integer(), default=0))

def downgrade():
    op.drop_table('reviews')
    
    with op.batch_alter_table('shops', schema=None) as batch_op:
        batch_op.drop_column('average_rating')
        batch_op.drop_column('review_count')
    
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_column('average_rating')
        batch_op.drop_column('review_count')
