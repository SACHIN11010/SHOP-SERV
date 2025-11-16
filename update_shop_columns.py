"""
This script updates the shops table with new columns.
Run this script to update your database schema.
"""
import sys
import os
from datetime import datetime

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.models import Shop

app = create_app()

def update_shop_columns():
    with app.app_context():
        # Add new columns to the shops table
        try:
            # Check if the columns exist before adding them
            inspector = db.inspect(db.engine)
            columns = [column['name'] for column in inspector.get_columns('shops')]
            
            # List of new columns to add
            new_columns = [
                'city', 'state', 'pincode', 'latitude', 'longitude',
                'contact_phone', 'contact_whatsapp', 'contact_email',
                'service_type', 'opening_time', 'closing_time',
                'is_delivery_available', 'is_pickup_available', 'is_cod_available',
                'delivery_radius_km', 'delivery_charge', 'min_order_amount',
                'is_verified'
            ]
            
            # Add columns that don't exist
            for column in new_columns:
                if column not in columns:
                    print(f"Adding column: {column}")
                    db.engine.execute(f"ALTER TABLE shops ADD COLUMN {column} {get_column_definition(column)}")
            
            print("Successfully updated the shops table!")
            
        except Exception as e:
            print(f"Error updating database: {str(e)}")
            db.session.rollback()
            raise

def get_column_definition(column_name):
    """Return the SQL data type for the given column name"""
    column_types = {
        'city': 'VARCHAR(100)',
        'state': 'VARCHAR(100)',
        'pincode': 'VARCHAR(20)',
        'latitude': 'FLOAT',
        'longitude': 'FLOAT',
        'contact_phone': 'VARCHAR(20)',
        'contact_whatsapp': 'VARCHAR(20)',
        'contact_email': 'VARCHAR(120)',
        'service_type': 'VARCHAR(50)',
        'opening_time': 'TIME',
        'closing_time': 'TIME',
        'is_delivery_available': 'BOOLEAN DEFAULT TRUE',
        'is_pickup_available': 'BOOLEAN DEFAULT TRUE',
        'is_cod_available': 'BOOLEAN DEFAULT TRUE',
        'delivery_radius_km': 'FLOAT DEFAULT 5.0',
        'delivery_charge': 'FLOAT DEFAULT 0.0',
        'min_order_amount': 'FLOAT DEFAULT 0.0',
        'is_verified': 'BOOLEAN DEFAULT FALSE'
    }
    return column_types.get(column_name, 'TEXT')

if __name__ == '__main__':
    print("Starting database update...")
    update_shop_columns()
    print("Database update completed!")
