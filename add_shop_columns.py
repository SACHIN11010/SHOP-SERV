import os
import sys
from datetime import datetime

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.models import Shop
from sqlalchemy import text

def add_shop_columns():
    app = create_app()
    
    with app.app_context():
        # Get the database engine
        engine = db.engine
        
        # Check if the shops table exists
        inspector = db.inspect(engine)
        if 'shops' not in inspector.get_table_names():
            print("Error: 'shops' table does not exist in the database.")
            return False
            
        # Get existing columns
        existing_columns = [column['name'] for column in inspector.get_columns('shops')]
        print("Existing columns in shops table:", existing_columns)
        
        # Define the columns we want to add
        columns_to_add = [
            'city', 'state', 'pincode', 'latitude', 'longitude',
            'contact_phone', 'contact_whatsapp', 'contact_email',
            'service_type', 'opening_time', 'closing_time',
            'is_delivery_available', 'is_pickup_available', 'is_cod_available',
            'delivery_radius_km', 'delivery_charge', 'min_order_amount',
            'is_verified'
        ]
        
        # Filter out columns that already exist
        columns_to_add = [col for col in columns_to_add if col not in existing_columns]
        
        if not columns_to_add:
            print("All columns already exist in the shops table.")
            return True
            
        print("Adding the following columns to the shops table:", columns_to_add)
        
        try:
            # Use raw SQL to add the columns
            with engine.connect() as connection:
                for column in columns_to_add:
                    # Determine the column type based on the model
                    column_type = 'VARCHAR(100)'
                    if column in ['latitude', 'longitude', 'delivery_charge', 'min_order_amount', 'delivery_radius_km']:
                        column_type = 'FLOAT'
                    elif column in ['opening_time', 'closing_time']:
                        column_type = 'TIME'
                    elif column in ['is_delivery_available', 'is_pickup_available', 'is_cod_available', 'is_verified']:
                        column_type = 'BOOLEAN DEFAULT FALSE'
                    
                    # Add the column using SQLAlchemy's text() function
                    sql = text(f"ALTER TABLE shops ADD COLUMN {column} {column_type}")
                    print(f"Executing: {sql}")
                    connection.execute(sql)
                
                # Commit the changes
                connection.commit()
                
            print("Successfully added all columns to the shops table.")
            return True
            
        except Exception as e:
            print(f"Error adding columns to shops table: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    print("Starting to add missing columns to shops table...")
    if add_shop_columns():
        print("Successfully updated the shops table!")
    else:
        print("Failed to update the shops table.")
        sys.exit(1)
