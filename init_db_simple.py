#!/usr/bin/env python3
"""
Simple database initialization script
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the app.py file as a module
import importlib.util
spec = importlib.util.spec_from_file_location("app_module", os.path.join(os.getcwd(), "app.py"))
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)

# Import models
from models import *

def init_db():
    """Initialize the database with all tables"""
    
    app = app_module.app
    db = app_module.db
    
    with app.app_context():
        print("Creating database tables...")
        
        # Create all tables
        db.create_all()
        
        print("Database tables created successfully!")
        
        # Check if shops table exists and show its structure
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        
        if 'shops' in inspector.get_table_names():
            print("\n✅ Shops table exists with columns:")
            for column in inspector.get_columns('shops'):
                print(f"   - {column['name']} ({column['type']})")
        else:
            print("❌ Shops table was not created")
        
        # Check if services table exists
        if 'services' in inspector.get_table_names():
            print("\n✅ Services table exists with columns:")
            for column in inspector.get_columns('services'):
                print(f"   - {column['name']} ({column['type']})")
        else:
            print("❌ Services table was not created")

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("\nDatabase initialization complete!")
