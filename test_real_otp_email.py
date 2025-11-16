#!/usr/bin/env python3
"""
Test script to send a real OTP email with the new HTML template
"""

import os
import sys
from flask import Flask, render_template
from dotenv import load_dotenv
from utils import send_email

# Load environment variables from .env file
load_dotenv()

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Create a minimal Flask app for testing
app = Flask(__name__)

# Load configuration from .env file
app.config['SECRET_KEY'] = 'test-secret-key'
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

def test_otp_email():
    """Test sending a real OTP email with the new template"""
    
    with app.app_context():
        # Test email recipient (change to your email for testing)
        test_email = "sachindarji2600@gmail.com"
        
        # Generate a test OTP (without database)
        import secrets
        import string
        otp_code = ''.join(secrets.choice(string.digits) for _ in range(6))
        
        # Mock user data
        user_name = "Test User"
        user_full_name = "Test User"  # Simulating user.full_name
        
        # Render the email template
        email_body = render_template('email/otp_template.html', 
                                   user_name=user_name,
                                   otp_code=otp_code,
                                   expiry_minutes=5,
                                   user_email=test_email,
                                   verification_url="http://localhost:5000/verify-otp",
                                   website_url="http://localhost:5000",
                                   support_url="http://localhost:5000/support",
                                   privacy_url="http://localhost:5000/privacy",
                                   facebook_url="#",
                                   twitter_url="#",
                                   instagram_url="#")
        
        # Send the email
        subject = "🧪 Test: New HTML OTP Template - SHOP&SERV"
        
        # Plain text fallback
        text_body = f"""
Test Password Reset Request - SHOP&SERV

Hello {user_name},

This is a test email to verify the new HTML template is working correctly.

Your test OTP code is: {otp_code}
This code will expire in 5 minutes.

If you didn't request this, please ignore this email.

For security reasons, never share this code with anyone.

© 2024 SHOP&SERV. All rights reserved.
        """
        
        print(f"📧 Sending test OTP email to: {test_email}")
        print(f"🔢 Test OTP code: {otp_code}")
        print(f"⏰ Code expires in: 5 minutes")
        
        success = send_email(test_email, subject, text_body, email_body)
        
        if success:
            print("\n✅ Test email sent successfully!")
            print("📬 Please check your inbox for the new formatted email")
            print("🎨 The email should feature:")
            print("   - Beautiful gradient design")
            print("   - Large, clear OTP code display")
            print("   - Security notices")
            print("   - Professional layout")
            print("   - Mobile-responsive design")
        else:
            print("\n❌ Failed to send test email")
            print("🔍 Please check your email configuration in .env file")
        
        return success

if __name__ == "__main__":
    print("🧪 Testing New HTML OTP Email Template")
    print("=" * 50)
    
    try:
        test_otp_email()
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        sys.exit(1)
