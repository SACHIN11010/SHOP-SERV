#!/usr/bin/env python3
"""
Test OTP functionality with new email credentials
"""

import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables
load_dotenv()

def test_email_config():
    """Test current email configuration"""
    print("=== Testing Email Configuration ===")
    print(f"MAIL_SERVER: {os.getenv('MAIL_SERVER')}")
    print(f"MAIL_PORT: {os.getenv('MAIL_PORT')}")
    print(f"MAIL_USERNAME: {os.getenv('MAIL_USERNAME')}")
    print(f"Password length: {len(os.getenv('MAIL_PASSWORD', ''))}")
    print(f"MAIL_DEFAULT_SENDER: {os.getenv('MAIL_DEFAULT_SENDER')}")
    
    # Test SMTP connection
    try:
        server = smtplib.SMTP(os.getenv('MAIL_SERVER'), int(os.getenv('MAIL_PORT')))
        server.starttls()
        
        username = os.getenv('MAIL_USERNAME')
        password = os.getenv('MAIL_PASSWORD')
        
        print(f"\nAttempting login with username: {username}")
        server.login(username, password)
        print("✅ SMTP login successful!")
        server.quit()
        return True
        
    except Exception as e:
        print(f"❌ SMTP login failed: {e}")
        return False

def send_test_email():
    """Send a test email"""
    try:
        msg = MIMEMultipart()
        msg['From'] = os.getenv('MAIL_DEFAULT_SENDER')
        msg['To'] = os.getenv('MAIL_USERNAME')  # Send to self for testing
        msg['Subject'] = 'SHOP&SERV OTP Test'
        
        body = """
        This is a test email from SHOP&SERV application.
        
        Your OTP code is: 123456
        
        If you received this email, the email configuration is working correctly!
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(os.getenv('MAIL_SERVER'), int(os.getenv('MAIL_PORT')))
        server.starttls()
        server.login(os.getenv('MAIL_USERNAME'), os.getenv('MAIL_PASSWORD'))
        
        text = msg.as_string()
        server.sendmail(os.getenv('MAIL_DEFAULT_SENDER'), os.getenv('MAIL_USERNAME'), text)
        server.quit()
        
        print("✅ Test email sent successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send test email: {e}")
        return False

if __name__ == "__main__":
    print("SHOP&SERV Email OTP Setup Test")
    print("=" * 40)
    
    # Test configuration
    config_ok = test_email_config()
    
    if config_ok:
        # Send test email
        send_test_email()
    else:
        print("\n🔧 Please fix the email configuration first.")
        print("\nTo fix this issue:")
        print("1. Enable 2-Step Verification on your Gmail account")
        print("2. Generate a new App Password at: https://myaccount.google.com/apppasswords")
        print("3. Use the 16-character App Password (no spaces) in your .env file")
        print("4. Update the .env file with the correct App Password")
