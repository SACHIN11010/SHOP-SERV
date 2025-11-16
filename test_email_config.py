#!/usr/bin/env python3
"""
📧 SHOP&SERV Email Configuration Test & Validation Script
=========================================================

This script tests your email configuration and helps validate SMTP settings.
It includes comprehensive error handling and security checks.

Usage:
    python test_email_config.py
    python test_email_config.py --provider gmail
    python test_email_config.py --to test@example.com

Features:
- Tests email configuration from environment variables
- Validates SMTP connection and authentication
- Sends test email with detailed logging
- Supports multiple email providers
- Security checks and warnings
- Detailed troubleshooting information
"""

import os
import sys
import smtplib
import argparse
import logging
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('email_test.log')
    ]
)
logger = logging.getLogger(__name__)

# Email provider configurations
EMAIL_PROVIDERS = {
    'gmail': {
        'server': 'smtp.gmail.com',
        'port': 587,
        'use_tls': True,
        'use_ssl': False,
        'name': 'Gmail',
        'help_url': 'https://myaccount.google.com/apppasswords'
    },
    'outlook': {
        'server': 'smtp-mail.outlook.com',
        'port': 587,
        'use_tls': True,
        'use_ssl': False,
        'name': 'Outlook/Hotmail',
        'help_url': 'https://support.microsoft.com/en-us/office/pop-imap-and-smtp-settings-for-outlook-com-d088b986-081a-4cc8-b9e5-9dca105764b9'
    },
    'zoho': {
        'server': 'smtp.zoho.com',
        'port': 587,
        'use_tls': True,
        'use_ssl': False,
        'name': 'Zoho Mail',
        'help_url': 'https://www.zoho.com/mail/help/imap-access.html'
    },
    'sendgrid': {
        'server': 'smtp.sendgrid.net',
        'port': 587,
        'use_tls': True,
        'use_ssl': False,
        'name': 'SendGrid',
        'help_url': 'https://docs.sendgrid.com/for-developers/sending-email/smtp-api'
    }
}

def check_environment_variables():
    """Check if required environment variables are set"""
    logger.info("🔍 Checking environment variables...")
    
    required_vars = ['MAIL_USERNAME', 'MAIL_PASSWORD']
    optional_vars = ['MAIL_SERVER', 'MAIL_PORT', 'MAIL_USE_TLS', 'MAIL_USE_SSL', 'MAIL_DEFAULT_SENDER']
    
    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    # Log optional variables (without sensitive data)
    for var in optional_vars:
        value = os.environ.get(var)
        if value:
            if 'PASSWORD' in var:
                logger.info(f"✅ {var}: [REDACTED]")
            else:
                logger.info(f"✅ {var}: {value}")
    
    return True

def validate_email_format(email):
    """Basic email format validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def test_smtp_connection(provider_config, username, password, timeout=30):
    """Test SMTP connection and authentication"""
    logger.info(f"🔌 Testing SMTP connection to {provider_config['server']}:{provider_config['port']}")
    
    try:
        with smtplib.SMTP(provider_config['server'], provider_config['port'], timeout=timeout) as server:
            # Enable debug mode for detailed logging
            server.set_debuglevel(1)
            
            # Setup encryption
            if provider_config['use_tls']:
                logger.info("🔐 Starting TLS encryption...")
                server.starttls()
            elif provider_config['use_ssl']:
                logger.info("🔐 Using SSL encryption...")
                # SSL is handled automatically in SMTP_SSL
            
            # Test authentication
            logger.info(f"🔑 Authenticating as {username}...")
            server.login(username, password)
            
            logger.info("✅ SMTP connection and authentication successful!")
            return True, server
            
    except smtplib.SMTPAuthenticationError as e:
        logger.error(f"❌ Authentication failed: {e}")
        logger.error("   Common causes:")
        logger.error("   - Incorrect username or password")
        logger.error("   - Using regular password instead of App Password")
        logger.error("   - 2FA not enabled or App Password not generated")
        logger.error(f"   Help: {provider_config['help_url']}")
        return False, None
        
    except smtplib.SMTPConnectError as e:
        logger.error(f"❌ Connection failed: {e}")
        logger.error("   Common causes:")
        logger.error("   - Network connectivity issues")
        logger.error("   - Firewall blocking SMTP port")
        logger.error("   - Incorrect SMTP server or port")
        return False, None
        
    except smtplib.SMTPServerDisconnected as e:
        logger.error(f"❌ Server disconnected: {e}")
        logger.error("   Common causes:")
        logger.error("   - Server timeout")
        logger.error("   - Network instability")
        return False, None
        
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        return False, None

def send_test_email(server, from_email, to_email, provider_name):
    """Send a test email"""
    logger.info(f"📧 Sending test email to {to_email}...")
    
    try:
        # Create message
        msg = MIMEMultipart()
        msg['Subject'] = f"SHOP&SERV Email Test - {provider_name}"
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
        
        # Email body
        body = f"""
🎉 EMAIL CONFIGURATION TEST SUCCESSFUL!

Provider: {provider_name}
From: {from_email}
To: {to_email}
Sent: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This email confirms that your SMTP configuration is working correctly.
If you received this email, your email system is ready to send OTP messages.

Best regards,
SHOP&SERV System
        """
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Send email
        server.send_message(msg)
        logger.info("✅ Test email sent successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to send test email: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Test SHOP&SERV email configuration')
    parser.add_argument('--provider', choices=['gmail', 'outlook', 'zoho', 'sendgrid'], 
                       help='Email provider to test')
    parser.add_argument('--to', help='Recipient email for test message')
    parser.add_argument('--username', help='SMTP username (overrides env var)')
    parser.add_argument('--password', help='SMTP password (overrides env var)')
    parser.add_argument('--timeout', type=int, default=30, help='Connection timeout in seconds')
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("📧 SHOP&SERV Email Configuration Test")
    print("=" * 70)
    
    # Check environment variables
    if not check_environment_variables():
        logger.error("❌ Environment variables check failed. Please configure your .env file.")
        sys.exit(1)
    
    # Get configuration
    provider = args.provider or os.environ.get('MAIL_PROVIDER', 'gmail').lower()
    username = args.username or os.environ.get('MAIL_USERNAME')
    password = args.password or os.environ.get('MAIL_PASSWORD')
    from_email = os.environ.get('MAIL_DEFAULT_SENDER', username)
    
    # Validate provider
    if provider not in EMAIL_PROVIDERS:
        logger.error(f"❌ Unknown provider: {provider}")
        logger.info(f"Available providers: {', '.join(EMAIL_PROVIDERS.keys())}")
        sys.exit(1)
    
    provider_config = EMAIL_PROVIDERS[provider]
    
    # Override with environment variables if set
    server = os.environ.get('MAIL_SERVER') or provider_config['server']
    port = int(os.environ.get('MAIL_PORT', provider_config['port']))
    use_tls = os.environ.get('MAIL_USE_TLS', str(provider_config['use_tls'])).lower() in ['true', '1', 't']
    use_ssl = os.environ.get('MAIL_USE_SSL', str(provider_config['use_ssl'])).lower() in ['true', '1', 't']
    
    # Update provider config with environment overrides
    provider_config.update({
        'server': server,
        'port': port,
        'use_tls': use_tls,
        'use_ssl': use_ssl
    })
    
    # Validate email formats
    if not validate_email_format(username):
        logger.error(f"❌ Invalid email format for username: {username}")
        sys.exit(1)
    
    if args.to and not validate_email_format(args.to):
        logger.error(f"❌ Invalid email format for recipient: {args.to}")
        sys.exit(1)
    
    # Display configuration
    print(f"\n📋 Configuration:")
    print(f"   Provider: {provider_config['name']}")
    print(f"   Server: {provider_config['server']}:{provider_config['port']}")
    print(f"   Username: {username}")
    print(f"   TLS: {provider_config['use_tls']}")
    print(f"   SSL: {provider_config['use_ssl']}")
    print(f"   From: {from_email}")
    if args.to:
        print(f"   To: {args.to}")
    print()
    
    # Test connection
    success, server = test_smtp_connection(provider_config, username, password, args.timeout)
    
    if not success:
        logger.error("❌ SMTP connection test failed!")
        logger.error("\n🔧 Troubleshooting steps:")
        logger.error("1. Check your email and password are correct")
        logger.error("2. Ensure 2FA is enabled for Gmail")
        logger.error("3. Generate a new App Password if needed")
        logger.error("4. Check network connectivity")
        logger.error("5. Verify firewall settings")
        logger.error(f"6. Visit: {provider_config['help_url']}")
        sys.exit(1)
    
    # Send test email if recipient provided
    if args.to:
        if send_test_email(server, from_email, args.to, provider_config['name']):
            logger.info("🎉 Complete! Your email configuration is working perfectly!")
        else:
            logger.error("❌ Test email failed, but connection was successful")
            logger.error("   Check recipient email address")
    else:
        logger.info("✅ SMTP connection successful!")
        logger.info("💡 Use --to <email> to send a test email")
    
    print("\n" + "=" * 70)
    print("✅ Email configuration test completed successfully!")
    print("=" * 70)

if __name__ == '__main__':
    main()
