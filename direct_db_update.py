"""
Direct database update script for the shops table.
This script connects directly to the SQLite database and adds the required columns.
"""
import sqlite3
import os

# Path to your SQLite database
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'site.db')

def add_columns():
    """Add new columns to the shops table if they don't exist"""
    # SQL statements to add columns if they don't exist
    alter_statements = [
        "ALTER TABLE shops ADD COLUMN IF NOT EXISTS city VARCHAR(100)",
        "ALTER TABLE shops ADD COLUMN IF NOT EXISTS state VARCHAR(100)",
        "ALTER TABLE shops ADD COLUMN IF NOT EXISTS pincode VARCHAR(20)",
        "ALTER TABLE shops ADD COLUMN IF NOT EXISTS latitude FLOAT",
        "ALTER TABLE shops ADD COLUMN IF NOT EXISTS longitude FLOAT",
        "ALTER TABLE shops ADD COLUMN IF NOT EXISTS contact_phone VARCHAR(20)",
        "ALTER TABLE shops ADD COLUMN IF NOT EXISTS contact_whatsapp VARCHAR(20)",
        "ALTER TABLE shops ADD COLUMN IF NOT EXISTS contact_email VARCHAR(120)",
        "ALTER TABLE shops ADD COLUMN IF NOT EXISTS service_type VARCHAR(50)",
        "ALTER TABLE shops ADD COLUMN IF NOT EXISTS opening_time TIME",
        "ALTER TABLE shops ADD COLUMN IF NOT EXISTS closing_time TIME",
        "ALTER TABLE shops ADD COLUMN IF NOT EXISTS is_delivery_available BOOLEAN DEFAULT 1",
        "ALTER TABLE shops ADD COLUMN IF NOT EXISTS is_pickup_available BOOLEAN DEFAULT 1",
        "ALTER TABLE shops ADD COLUMN IF NOT EXISTS is_cod_available BOOLEAN DEFAULT 1",
        "ALTER TABLE shops ADD COLUMN IF NOT EXISTS delivery_radius_km FLOAT DEFAULT 5.0",
        "ALTER TABLE shops ADD COLUMN IF NOT EXISTS delivery_charge FLOAT DEFAULT 0.0",
        "ALTER TABLE shops ADD COLUMN IF NOT EXISTS min_order_amount FLOAT DEFAULT 0.0",
        "ALTER TABLE shops ADD COLUMN IF NOT EXISTS is_verified BOOLEAN DEFAULT 0"
    ]
    
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Execute each ALTER TABLE statement
        for statement in alter_statements:
            try:
                cursor.execute(statement)
                print(f"Executed: {statement}")
            except sqlite3.OperationalError as e:
                print(f"Skipped (column may already exist): {e}")
                continue
        
        # Commit the changes
        conn.commit()
        print("\nDatabase update completed successfully!")
        
    except Exception as e:
        print(f"Error updating database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    print("Starting database update...")
    print(f"Database path: {DB_PATH}")
    
    # Check if database file exists
    if not os.path.exists(DB_PATH):
        print(f"Error: Database file not found at {DB_PATH}")
        print("Please make sure you're running this script from the correct directory.")
    else:
        add_columns()
    
    print("\nScript execution completed. Press Enter to exit...")
    input()
