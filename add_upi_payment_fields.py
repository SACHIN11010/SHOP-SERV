import os
import sys
from datetime import datetime

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from sqlalchemy import text

def add_upi_payment_fields():
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
        
        # Define the UPI payment fields to add
        upi_fields = [
            'upi_id',
            'upi_qr_code',
            'bank_name',
            'account_holder_name',
            'account_number',
            'ifsc_code',
            'preferred_payment_method'  # upi, bank_transfer, etc.
        ]
        
        # Filter out columns that already exist
        fields_to_add = [field for field in upi_fields if field not in existing_columns]
        
        if not fields_to_add:
            print("All UPI payment fields already exist in the shops table.")
            return True
            
        print("Adding the following UPI payment fields to the shops table:", fields_to_add)
        
        try:
            # Use raw SQL to add the columns
            with engine.connect() as connection:
                for field in fields_to_add:
                    # Determine the column type based on the field
                    column_type = 'VARCHAR(255)'
                    if field == 'preferred_payment_method':
                        column_type = 'VARCHAR(50) DEFAULT "upi"'
                    
                    # Add the column using SQLAlchemy's text() function
                    sql = text(f"ALTER TABLE shops ADD COLUMN {field} {column_type}")
                    print(f"Executing: {sql}")
                    connection.execute(sql)
                
                # Commit the changes
                connection.commit()
                
            print("Successfully added UPI payment fields to the shops table.")
            return True
            
        except Exception as e:
            print(f"Error adding UPI payment fields to shops table: {str(e)}")
            import traceback
            traceback.print_exc()
            return False

if __name__ == '__main__':
    print("Starting to add UPI payment fields to shops table...")
    if add_upi_payment_fields():
        print("Successfully updated the shops table with UPI payment fields!")
    else:
        print("Failed to update the shops table with UPI payment fields.")
        sys.exit(1)
