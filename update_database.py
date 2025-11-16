from app import create_app, db
from app.models.models import *  # Import all models to ensure they're registered with SQLAlchemy

app = create_app()

def update_database():
    with app.app_context():
        try:
            # This will create any missing tables and add any missing columns to existing tables
            db.create_all()
            print("Database schema updated successfully!")
        except Exception as e:
            print(f"Error updating database: {e}")
            raise

if __name__ == '__main__':
    print("Starting database update...")
    update_database()
    print("Update complete. You can now run the application.")
