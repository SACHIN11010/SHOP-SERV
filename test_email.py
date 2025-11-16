"""Test email configuration"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("🔄 Testing email configuration...\n")

# Email settings
MAIL_USERNAME = "sachindarji2600@gmail.com"
MAIL_PASSWORD = "lnypalanymxnlafk"
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587

try:
    # Create test message
    msg = MIMEMultipart()
    msg['Subject'] = "✅ SHOP&SERV Email Test - Configuration Successful"
    msg['From'] = MAIL_USERNAME
    msg['To'] = MAIL_USERNAME
    
    body = """
    <html>
    <body>
        <h2 style="color: #28a745;">✅ Email Configuration Successful!</h2>
        <p>Your SHOP&SERV email system is now properly configured.</p>
        <p><strong>Email:</strong> sachindarji2600@gmail.com</p>
        <p><strong>Status:</strong> Ready to send OTP emails</p>
        <hr>
        <p>You can now use the <strong>Forgot Password</strong> feature.</p>
        <p>OTP emails will be sent to registered users automatically.</p>
        <br>
        <p style="color: #666; font-size: 12px;">This is a test email from SHOP&SERV</p>
    </body>
    </html>
    """
    
    msg.attach(MIMEText(body, 'html'))
    
    # Send email
    print("📧 Connecting to Gmail SMTP server...")
    with smtplib.SMTP(MAIL_SERVER, MAIL_PORT) as server:
        server.starttls()
        print("🔐 Authenticating...")
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        print("📤 Sending test email...")
        server.send_message(msg)
    
    print("\n" + "="*60)
    print("✅ SUCCESS! Email sent successfully!")
    print("="*60)
    print(f"\n📬 Check your inbox: {MAIL_USERNAME}")
    print("📧 Subject: '✅ SHOP&SERV Email Test - Configuration Successful'")
    print("\n✨ Your forgot password system is fully functional!")
    print("\n🚀 Next steps:")
    print("1. Check your email inbox")
    print("2. Restart your Flask app: python app.py")
    print("3. Test forgot password feature")
    print("4. OTP will be sent to registered emails")
    
except smtplib.SMTPAuthenticationError:
    print("\n❌ Authentication failed!")
    print("Please check:")
    print("1. App Password is correct")
    print("2. 2-Step Verification is enabled")
    print("3. Try generating a new App Password")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nPlease check your internet connection and try again.")
