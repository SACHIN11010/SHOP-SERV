#!/usr/bin/env python3
"""
Test the new professional OTP email
"""

import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, '.')

# Import app modules
import app as app_module

def test_otp_email():
    """Test the new OTP email function"""
    print("=== Testing Professional OTP Email ===")
    
    load_dotenv()
    
    with app_module.app.app_context():
        try:
            from utils import send_otp_email
            
            # Test sending OTP email
            test_email = 'shopsnservices@gmail.com'
            test_name = 'Test User'
            test_otp = '123456'
            
            print(f"Sending OTP email to {test_email}...")
            success = send_otp_email(test_email, test_name, test_otp)
            
            if success:
                print("✅ Professional OTP email sent successfully!")
                print("📧 Check your inbox for the beautifully formatted email")
            else:
                print("❌ Failed to send OTP email")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_otp_email()
