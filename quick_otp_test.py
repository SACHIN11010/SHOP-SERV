#!/usr/bin/env python3
"""
Quick test of OTP email with professional template
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_otp_email():
    """Test OTP email directly"""
    print("=== Testing Professional OTP Email ===")
    
    # Import and run app
    exec(open('app.py').read())
    
    with app.app_context():
        try:
            from utils import send_otp_email, create_otp
            
            # Create real OTP
            test_email = 'shopsnservices@gmail.com'
            test_name = 'SHOP&SERV User'
            otp_code = create_otp(test_email)
            
            print(f"Generated OTP: {otp_code}")
            print(f"Sending professional email to {test_email}...")
            
            success = send_otp_email(test_email, test_name, otp_code)
            
            if success:
                print("✅ Professional OTP email sent successfully!")
                print("📧 Check your inbox for the beautifully formatted email")
                print("🎨 The email includes:")
                print("   - Responsive design for all devices")
                print("   - Large, clear OTP code")
                print("   - Professional branding")
                print("   - Security notice")
                print("   - Social media links")
            else:
                print("❌ Failed to send OTP email")
                
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_otp_email()
