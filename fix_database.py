import os
import sys
from sqlalchemy import create_engine, MetaData, Table, Column, String, Boolean, Float, Time
from sqlalchemy.orm import sessionmaker

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Database configuration - update this with your actual database URI
DATABASE_URI = 'sqlite:///instance/site.db'

def add_missing_columns():
    # Create an engine that connects to the database
    engine = create_engine(DATABASE_URI)
    metadata = MetaData()
    
    # Reflect the existing database
    metadata.reflect(bind=engine)
    
    # Define the columns we want to add
    columns_to_add = [
        ('city', String(100)),
        ('state', String(100)),
        ('pincode', String(20)),
        ('latitude', Float),
        ('longitude', Float),
        ('contact_phone', String(20)),
        ('contact_whatsapp', String(20)),
        ('contact_email', String(120)),
        ('service_type', String(50)),
        ('opening_time', Time),
        ('closing_time', Time),
        ('is_delivery_available', Boolean, True),
        ('is_pickup_available', Boolean, True),
        ('is_cod_available', Boolean, True),
        ('delivery_radius_km', Float, 5.0),
        ('delivery_charge', Float, 0.0),
        ('min_order_amount', Float, 0.0),
        ('is_verified', Boolean, False)
    ]
    
    # Get the shops table
    if 'shops' in metadata.tables:
        shops_table = Table('shops', metadata, autoload_with=engine)
        
        # Check and add each column if it doesn't exist
        with engine.connect() as connection:
            for col_def in columns_to_add:
                column_name = col_def[0]
                column_type = col_def[1]
                
                # Check if column exists
                if column_name not in shops_table.columns:
                    # Get default value if specified
                    default_value = col_def[2] if len(col_def) > 2 else None
                    
                    # Add the column
                    print(f"Adding column: {column_name}")
                    column = Column(column_name, column_type, default=default_value)
                    column.create(engine, checkfirst=True)
                    
                    print(f"Successfully added column: {column_name}")
                else:
                    print(f"Column {column_name} already exists, skipping...")
        
        print("\nDatabase update completed successfully!")
    else:
        print("Error: 'shops' table not found in the database.")

if __name__ == '__main__':
    print("Starting database update...")
    add_missing_columns()
    print("Done!")
