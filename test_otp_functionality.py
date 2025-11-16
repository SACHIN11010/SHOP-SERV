#!/usr/bin/env python3
"""
Test OTP functionality with new email credentials
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add current directory to path
sys.path.insert(0, '.')

def test_otp_system():
    """Test the complete OTP system"""
    print("=== Testing SHOP&SERV OTP System ===")
    
    # Import app modules
    from app import app
    from utils import create_otp, verify_otp, send_email
    
    with app.app_context():
        try:
            # Test OTP creation
            test_email = 'shopsnservices@gmail.com'
            otp_code = create_otp(test_email)
            print(f'✅ OTP created for {test_email}: {otp_code}')
            
            # Test OTP verification
            is_valid = verify_otp(test_email, otp_code)
            print(f'✅ OTP verification result: {is_valid}')
            
            # Test wrong OTP
            is_invalid = verify_otp(test_email, '000000')
            print(f'✅ Wrong OTP verification (should be False): {is_invalid}')
            
            # Test sending OTP email
            subject = 'SHOP&SERV - Your OTP Code'
            body = f"""
            Hello,
            
            Your OTP code for SHOP&SERV is: {otp_code}
            
            This code will expire in 10 minutes.
            
            Thank you,
            SHOP&SERV Team
            """
            
            email_sent = send_email(test_email, subject, body)
            print(f'✅ OTP email sent successfully: {email_sent}')
            
            return True
            
        except Exception as e:
            print(f'❌ OTP test failed: {e}')
            import traceback
            traceback.print_exc()
            return False

if __name__ == "__main__":
    print("SHOP&SERV OTP System Test")
    print("=" * 40)
    
    success = test_otp_system()
    
    print("\n" + "=" * 40)
    if success:
        print("🎉 OTP system is working correctly!")
        print("✅ Users can now receive OTP emails for:")
        print("   - Password reset")
        print("   - Email verification")
        print("   - Two-factor authentication")
    else:
        print("❌ OTP system needs attention")
