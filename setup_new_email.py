#!/usr/bin/env python3
"""
Setup new email credentials for SHOP&SERV
"""

import os
from dotenv import load_dotenv

def create_env_file():
    """Create .env file with new credentials"""
    env_content = """SECRET_KEY=your-secret-key-here-change-this-in-production-use-random-string
STRIPE_PUBLIC_KEY=pk_test_your_stripe_public_key_here
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key_here
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=shosnservices@gmail.com
MAIL_PASSWORD=YOUR_16_CHARACTER_APP_PASSWORD_HERE
MAIL_DEFAULT_SENDER=shosnservices@gmail.com
UPI_ID=6351074394@upi
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created with placeholder for App Password")
    print("\n📋 Next Steps:")
    print("1. Go to: https://myaccount.google.com/apppasswords")
    print("2. Sign in to your Google account")
    print("3. Under 'Select app', choose 'Other (Custom name)'")
    print("4. Enter 'SHOP&SERV' as the app name")
    print("5. Click 'Generate'")
    print("6. Copy the 16-character password (no spaces)")
    print("7. Update the .env file replacing 'YOUR_16_CHARACTER_APP_PASSWORD_HERE'")
    print("8. Run: python test_otp_setup.py")

def test_current_setup():
    """Test current email setup"""
    load_dotenv()
    
    print("=== Current Email Configuration ===")
    print(f"Email: {os.getenv('MAIL_USERNAME')}")
    print(f"Password length: {len(os.getenv('MAIL_PASSWORD', ''))}")
    
    if os.getenv('MAIL_PASSWORD') == 'YOUR_16_CHARACTER_APP_PASSWORD_HERE':
        print("❌ Please replace the placeholder with your actual App Password")
        return False
    
    # Test SMTP connection
    import smtplib
    try:
        server = smtplib.SMTP(os.getenv('MAIL_SERVER'), int(os.getenv('MAIL_PORT')))
        server.starttls()
        server.login(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD'))
        server.quit()
        print("✅ Email configuration is working!")
        return True
    except Exception as e:
        print(f"❌ Email test failed: {e}")
        return False

if __name__ == "__main__":
    print("SHOP&SERV Email Setup Helper")
    print("=" * 40)
    
    # Check if .env exists
    if not os.path.exists('.env'):
        print("Creating new .env file...")
        create_env_file()
    else:
        print("Testing current setup...")
        test_current_setup()
