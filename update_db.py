import os
import sys
from datetime import datetime

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.models import *  # Import all models to ensure they're registered with SQLAlchemy

def update_database():
    app = create_app()
    
    with app.app_context():
        try:
            # This will create any missing tables and add any missing columns to existing tables
            db.create_all()
            print("Database schema has been updated successfully!")
            
            # Verify the shops table has the expected columns
            inspector = db.inspect(db.engine)
            if 'shops' in inspector.get_table_names():
                columns = [column['name'] for column in inspector.get_columns('shops')]
                print("Shops table columns:", columns)
                
        except Exception as e:
            print(f"Error updating database: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    return True

if __name__ == '__main__':
    print("Updating database schema...")
    if update_database():
        print("Database update completed successfully!")
    else:
        print("Database update failed.")
        sys.exit(1)
    print("Done!")
