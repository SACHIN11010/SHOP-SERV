"""
Setup script for SHOP&SERV
Run this script to initialize the application
"""
import os
import secrets

def create_directories():
    """Create necessary directories"""
    directories = [
        'static/uploads',
        'static/uploads/products',
        'static/uploads/shops',
        'instance'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def generate_secret_key():
    """Generate a random secret key"""
    return secrets.token_hex(32)

def setup_env_file():
    """Setup .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        print("\n⚠️  .env file not found!")
        print("Please create a .env file with the following variables:")
        print("\nSECRET_KEY=your-secret-key")
        print("STRIPE_PUBLIC_KEY=your-stripe-public-key")
        print("STRIPE_SECRET_KEY=your-stripe-secret-key")
        print("MAIL_USERNAME=your-email@gmail.com")
        print("MAIL_PASSWORD=your-gmail-app-password")
        print("MAIL_DEFAULT_SENDER=your-email@gmail.com")
        print("\nGenerated SECRET_KEY for you:")
        print(generate_secret_key())
    else:
        print("✓ .env file exists")

def main():
    print("=" * 50)
    print("SHOP&SERV Setup")
    print("=" * 50)
    
    print("\n1. Creating directories...")
    create_directories()
    
    print("\n2. Checking environment file...")
    setup_env_file()
    
    print("\n" + "=" * 50)
    print("Setup complete!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Configure your .env file with proper credentials")
    print("2. Run: pip install -r requirements.txt")
    print("3. Run: python app.py")
    print("4. Visit: http://localhost:5000")
    print("\nDefault admin login:")
    print("Email: admin@shopserv.com")
    print("Password: admin123")
    print("=" * 50)

if __name__ == '__main__':
    main()
