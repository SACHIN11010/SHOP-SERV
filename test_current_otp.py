#!/usr/bin/env python3
"""
Test current OTP functionality in the SHOP&SERV application
"""

import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Import app modules
from app import create_app
from utils import create_otp, verify_otp, send_email

def test_otp_creation():
    """Test OTP creation functionality"""
    print("=== Testing OTP Creation ===")
    
    app = create_app()
    
    with app.app_context():
        try:
            test_email = "shosnservices@gmail.com"
            otp_code = create_otp(test_email)
            print(f"✅ OTP created successfully: {otp_code}")
            return otp_code
        except Exception as e:
            print(f"❌ Failed to create OTP: {e}")
            return None

def test_otp_verification(otp_code):
    """Test OTP verification functionality"""
    print("\n=== Testing OTP Verification ===")
    
    app = create_app()
    
    with app.app_context():
        try:
            test_email = "shosnservices@gmail.com"
            is_valid = verify_otp(test_email, otp_code)
            print(f"✅ OTP verification result: {is_valid}")
            return is_valid
        except Exception as e:
            print(f"❌ Failed to verify OTP: {e}")
            return False

def test_email_sending():
    """Test email sending functionality"""
    print("\n=== Testing Email Sending ===")
    
    app = create_app()
    
    with app.app_context():
        try:
            test_email = "shosnservices@gmail.com"
            subject = "SHOP&SERV OTP Test"
            body = """
            This is a test email from SHOP&SERV.
            
            Your OTP code is: 123456
            
            Thank you for using SHOP&SERV!
            """
            
            success = send_email(test_email, subject, body)
            if success:
                print("✅ Email sent successfully!")
            else:
                print("❌ Failed to send email")
            return success
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            return False

if __name__ == "__main__":
    print("SHOP&SERV OTP System Test")
    print("=" * 40)
    
    # Test OTP creation
    otp_code = test_otp_creation()
    
    if otp_code:
        # Test OTP verification
        test_otp_verification(otp_code)
    
    # Test email sending
    test_email_sending()
    
    print("\n" + "=" * 40)
    print("Test completed!")
    print("\nNote: If email sending fails, you need to:")
    print("1. Enable 2-Step Verification on shosnservices@gmail.com")
    print("2. Generate a new App Password at: https://myaccount.google.com/apppasswords")
    print("3. Update the .env file with the correct 16-character App Password")
