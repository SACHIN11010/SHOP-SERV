"""
Interactive Email Configuration Setup for SHOP&SERV
This script helps you configure Gmail for sending OTP emails.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_email_connection(username, password, test_email):
    """Test if email credentials work"""
    try:
        print("\n🔄 Testing email connection...")
        
        # Create test message
        msg = MIMEMultipart()
        msg['Subject'] = "SHOP&SERV Email Configuration Test"
        msg['From'] = username
        msg['To'] = test_email
        
        body = """
        <h2>Email Configuration Successful!</h2>
        <p>Your SHOP&SERV email is now properly configured.</p>
        <p>You can now send OTP emails for password reset.</p>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Connect and send
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
        
        print("✅ Email sent successfully!")
        print(f"📧 Check your inbox at: {test_email}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed! Check your email and app password.")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def update_env_file(username, password):
    """Update .env file with email credentials"""
    try:
        env_path = '.env'
        
        # Read existing .env
        if os.path.exists(env_path):
            with open(env_path, 'r') as f:
                lines = f.readlines()
        else:
            lines = []
        
        # Update or add email settings
        updated_lines = []
        settings_updated = {
            'MAIL_USERNAME': False,
            'MAIL_PASSWORD': False,
            'MAIL_DEFAULT_SENDER': False
        }
        
        for line in lines:
            if line.startswith('MAIL_USERNAME='):
                updated_lines.append(f'MAIL_USERNAME={username}\n')
                settings_updated['MAIL_USERNAME'] = True
            elif line.startswith('MAIL_PASSWORD='):
                updated_lines.append(f'MAIL_PASSWORD={password}\n')
                settings_updated['MAIL_PASSWORD'] = True
            elif line.startswith('MAIL_DEFAULT_SENDER='):
                updated_lines.append(f'MAIL_DEFAULT_SENDER={username}\n')
                settings_updated['MAIL_DEFAULT_SENDER'] = True
            else:
                updated_lines.append(line)
        
        # Add missing settings
        if not settings_updated['MAIL_USERNAME']:
            updated_lines.append(f'MAIL_USERNAME={username}\n')
        if not settings_updated['MAIL_PASSWORD']:
            updated_lines.append(f'MAIL_PASSWORD={password}\n')
        if not settings_updated['MAIL_DEFAULT_SENDER']:
            updated_lines.append(f'MAIL_DEFAULT_SENDER={username}\n')
        
        # Write back to .env
        with open(env_path, 'w') as f:
            f.writelines(updated_lines)
        
        print("✅ .env file updated successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error updating .env: {e}")
        return False

def main():
    print("=" * 60)
    print("📧 SHOP&SERV Email Configuration Setup")
    print("=" * 60)
    print("\nThis script will help you configure Gmail for sending OTP emails.")
    print("\n⚠️  IMPORTANT: You need a Gmail App Password (not your regular password)")
    print("\nSteps to get Gmail App Password:")
    print("1. Go to: https://myaccount.google.com/apppasswords")
    print("2. Enable 2-Step Verification if not already enabled")
    print("3. Create an App Password for 'Mail'")
    print("4. Copy the 16-character password")
    print("\n" + "=" * 60)
    
    # Get email
    print("\n📝 Enter your Gmail address:")
    email = input("Email: ").strip()
    
    if not email.endswith('@gmail.com'):
        print("⚠️  Warning: This setup is optimized for Gmail.")
        proceed = input("Continue anyway? (yes/no): ").strip().lower()
        if proceed != 'yes':
            print("Setup cancelled.")
            return
    
    # Get app password
    print("\n🔑 Enter your Gmail App Password (16 characters):")
    print("(Paste it here - spaces will be removed automatically)")
    password = input("App Password: ").strip().replace(' ', '')
    
    if len(password) != 16:
        print(f"⚠️  Warning: App password should be 16 characters (you entered {len(password)})")
        proceed = input("Continue anyway? (yes/no): ").strip().lower()
        if proceed != 'yes':
            print("Setup cancelled.")
            return
    
    # Test email
    print("\n📧 Enter an email address to send a test message:")
    test_email = input("Test Email: ").strip()
    
    # Test connection
    print("\n" + "=" * 60)
    if test_email_connection(email, password, test_email):
        print("\n" + "=" * 60)
        print("✅ Email configuration successful!")
        print("=" * 60)
        
        # Update .env
        save = input("\n💾 Save these settings to .env file? (yes/no): ").strip().lower()
        if save == 'yes':
            if update_env_file(email, password):
                print("\n🎉 Setup complete! Your email is now configured.")
                print("\n📌 Next steps:")
                print("1. Restart your Flask application")
                print("2. Test the 'Forgot Password' feature")
                print("3. OTP will be sent to registered email addresses")
            else:
                print("\n⚠️  Failed to update .env file. Please update manually:")
                print(f"MAIL_USERNAME={email}")
                print(f"MAIL_PASSWORD={password}")
                print(f"MAIL_DEFAULT_SENDER={email}")
        else:
            print("\nSettings not saved. Update .env manually:")
            print(f"MAIL_USERNAME={email}")
            print(f"MAIL_PASSWORD={password}")
            print(f"MAIL_DEFAULT_SENDER={email}")
    else:
        print("\n" + "=" * 60)
        print("❌ Email configuration failed!")
        print("=" * 60)
        print("\n🔍 Troubleshooting:")
        print("1. Make sure 2-Step Verification is enabled")
        print("2. Use App Password, not your regular Gmail password")
        print("3. Check if the App Password is correct (16 characters)")
        print("4. Try generating a new App Password")
        print("\n📖 Help: https://support.google.com/accounts/answer/185833")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
