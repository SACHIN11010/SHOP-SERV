#!/usr/bin/env python3
"""
Send OTP email with professional HTML template
"""

import os
from flask import render_template
from utils import send_email

def send_otp_email(user_email, user_name, otp_code, expiry_minutes=10):
    """Send OTP email with professional HTML template"""
    
    # Template data
    template_data = {
        'user_name': user_name or 'User',
        'user_email': user_email,
        'otp_code': otp_code,
        'expiry_minutes': expiry_minutes,
        'verification_url': 'https://your-shop-serv-site.com/verify',
        'website_url': 'https://your-shop-serv-site.com',
        'support_url': 'https://your-shop-serv-site.com/support',
        'privacy_url': 'https://your-shop-serv-site.com/privacy',
        'facebook_url': 'https://facebook.com/shopserv',
        'twitter_url': 'https://twitter.com/shopserv',
        'instagram_url': 'https://instagram.com/shopserv'
    }
    
    # Render HTML template
    html_body = render_template('email/otp_template.html', **template_data)
    
    # Plain text version
    text_body = f"""
Hello {user_name or 'User'}!

We received a request to verify your email address for your SHOP&SERV account.

Your verification code is: {otp_code}

This code will expire in {expiry_minutes} minutes.

Security Notice:
Never share this verification code with anyone. Our team will never ask for your verification code via email, phone, or any other method.

If you didn't request this code, please ignore this email or contact our support team immediately.

Visit our website: https://your-shop-serv-site.com
Contact Support: https://your-shop-serv-site.com/support

© 2024 SHOP&SERV. All rights reserved.
    """
    
    # Send email
    subject = "SHOP&SERV - Your Verification Code"
    success = send_email(
        to=user_email,
        subject=subject,
        body=text_body,
        html_body=html_body
    )
    
    return success

if __name__ == "__main__":
    # Test the OTP email
    import os
    import sys
    from dotenv import load_dotenv
    
    # Add current directory to path
    sys.path.insert(0, '.')
    
    # Import app modules
    import app as app_module
    
    load_dotenv()
    
    with app_module.app.app_context():
        # Test sending OTP email
        test_email = 'shopsnservices@gmail.com'
        test_name = 'Test User'
        test_otp = '123456'
        
        print("Sending test OTP email...")
        success = send_otp_email(test_email, test_name, test_otp)
        
        if success:
            print("✅ OTP email sent successfully!")
        else:
            print("❌ Failed to send OTP email")
