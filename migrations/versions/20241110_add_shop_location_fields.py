"""Add location and delivery fields to Shop

Revision ID: 20241110_add_shop_location_fields
Revises: 
Create Date: 2024-11-10 21:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = '20241110_add_shop_location_fields'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Add new columns to shops table
    with op.batch_alter_table('shops', schema=None) as batch_op:
        batch_op.add_column(sa.Column('city', sa.String(100), nullable=True))
        batch_op.add_column(sa.Column('state', sa.String(100), nullable=True))
        batch_op.add_column(sa.Column('pincode', sa.String(20), nullable=True))
        batch_op.add_column(sa.Column('latitude', sa.Float, nullable=True))
        batch_op.add_column(sa.Column('longitude', sa.Float, nullable=True))
        batch_op.add_column(sa.Column('delivery_radius_km', sa.Float, default=5.0))
        batch_op.add_column(sa.Column('delivery_charge', sa.Float, default=0.0))
        batch_op.add_column(sa.Column('min_order_amount', sa.Float, default=0.0))
        batch_op.add_column(sa.Column('opening_time', sa.Time, nullable=True))
        batch_op.add_column(sa.Column('closing_time', sa.Time, nullable=True))
        batch_op.add_column(sa.Column('is_verified', sa.Boolean, default=False))
        batch_op.add_column(sa.Column('service_type', sa.String(50), nullable=True))
        batch_op.add_column(sa.Column('contact_phone', sa.String(20), nullable=True))
        batch_op.add_column(sa.Column('contact_whatsapp', sa.String(20), nullable=True))
        batch_op.add_column(sa.Column('contact_email', sa.String(120), nullable=True))
        batch_op.add_column(sa.Column('is_delivery_available', sa.Boolean, default=True))
        batch_op.add_column(sa.Column('is_pickup_available', sa.Boolean, default=True))
        batch_op.add_column(sa.Column('is_cod_available', sa.Boolean, default=True))

def downgrade():
    with op.batch_alter_table('shops', schema=None) as batch_op:
        batch_op.drop_column('city')
        batch_op.drop_column('state')
        batch_op.drop_column('pincode')
        batch_op.drop_column('latitude')
        batch_op.drop_column('longitude')
        batch_op.drop_column('delivery_radius_km')
        batch_op.drop_column('delivery_charge')
        batch_op.drop_column('min_order_amount')
        batch_op.drop_column('opening_time')
        batch_op.drop_column('closing_time')
        batch_op.drop_column('is_verified')
        batch_op.drop_column('service_type')
        batch_op.drop_column('contact_phone')
        batch_op.drop_column('contact_whatsapp')
        batch_op.drop_column('contact_email')
        batch_op.drop_column('is_delivery_available')
        batch_op.drop_column('is_pickup_available')
        batch_op.drop_column('is_cod_available')
