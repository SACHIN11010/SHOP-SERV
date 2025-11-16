import os
import sys
from sqlalchemy import create_engine, inspect

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import your models and db
from app import create_app, db
from app.models.models import *  # This imports all your models

def init_db():
    # Create the Flask app
    app = create_app()
    
    with app.app_context():
        # This will create all tables that don't exist yet
        db.create_all()
        
        # Verify the shops table exists
        inspector = inspect(db.engine)
        if 'shops' in inspector.get_table_names():
            print("Shops table exists with the following columns:")
            for column in inspector.get_columns('shops'):
                print(f"- {column['name']} ({column['type']})")
        else:
            print("Shops table was not created. There might be an issue with your models.")

if __name__ == '__main__':
    print("Initializing database...")
    init_db()
    print("Database initialization complete!")
