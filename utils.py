import os
import secrets
import string
import smtplib
import time
import logging
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from werkzeug.utils import secure_filename
from flask import current_app
from app.models.models import db, OTP
from PIL import Image
import qrcode
import io
import base64
import requests

# Configure logging
logger = logging.getLogger(__name__)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_image(file, folder='products'):
    """Save uploaded image with secure filename"""
    if file and allowed_file(file.filename):
        # Generate unique filename
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(file.filename)
        filename = random_hex + f_ext
        
        # Create folder path
        folder_path = os.path.join(current_app.config['UPLOAD_FOLDER'], folder)
        os.makedirs(folder_path, exist_ok=True)
        
        # Save path
        file_path = os.path.join(folder_path, filename)
        
        # Resize and optimize image
        img = Image.open(file)
        
        # Convert RGBA to RGB if necessary
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Resize if too large
        max_size = (800, 800)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save optimized image
        img.save(file_path, quality=85, optimize=True)
        
        return f'{folder}/{filename}'
    return None

def delete_image(image_path):
    """Delete image file"""
    if image_path:
        full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_path)
        if os.path.exists(full_path):
            try:
                os.remove(full_path)
            except:
                pass

def generate_otp():
    """Generate 6-digit OTP"""
    return ''.join(secrets.choice(string.digits) for _ in range(6))

def create_otp(email):
    """Create and store OTP for email"""
    # Delete old OTPs for this email
    OTP.query.filter_by(email=email).delete()
    
    # Generate new OTP
    otp_code = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    
    otp = OTP(email=email, otp_code=otp_code, expires_at=expires_at)
    db.session.add(otp)
    db.session.commit()
    
    return otp_code

def verify_otp(email, otp_code):
    """Verify OTP code"""
    otp = OTP.query.filter_by(
        email=email,
        otp_code=otp_code,
        is_used=False
    ).first()
    
    if otp and otp.expires_at > datetime.utcnow():
        otp.is_used = True
        db.session.commit()
        return True
    return False

def get_email_provider_config():
    """Get email provider configuration based on MAIL_PROVIDER setting"""
    provider = current_app.config.get('MAIL_PROVIDER', 'gmail').lower()
    
    providers = {
        'gmail': {
            'server': 'smtp.gmail.com',
            'port': 587,
            'use_tls': True,
            'use_ssl': False,
            'name': 'Gmail'
        },
        'outlook': {
            'server': 'smtp-mail.outlook.com',
            'port': 587,
            'use_tls': True,
            'use_ssl': False,
            'name': 'Outlook'
        },
        'zoho': {
            'server': 'smtp.zoho.com',
            'port': 587,
            'use_tls': True,
            'use_ssl': False,
            'name': 'Zoho Mail'
        },
        'sendgrid': {
            'server': 'smtp.sendgrid.net',
            'port': 587,
            'use_tls': True,
            'use_ssl': False,
            'name': 'SendGrid'
        }
    }
    
    return providers.get(provider, providers['gmail'])

def send_email(to, subject, body, html_body=None, retries=None):
    """Send email using SMTP with retry logic and proper error handling"""
    if retries is None:
        retries = current_app.config.get('MAIL_MAX_RETRIES', 3)
    
    # Get email configuration securely
    mail_username = current_app.config.get('MAIL_USERNAME')
    mail_password = current_app.config.get('MAIL_PASSWORD')
    
    # Get provider config with environment overrides
    provider_config = get_email_provider_config()
    mail_server = current_app.config.get('MAIL_SERVER', provider_config['server'])
    mail_port = current_app.config.get('MAIL_PORT', provider_config['port'])
    mail_use_tls = current_app.config.get('MAIL_USE_TLS', provider_config['use_tls'])
    mail_use_ssl = current_app.config.get('MAIL_USE_SSL', provider_config['use_ssl'])
    mail_sender = current_app.config.get('MAIL_DEFAULT_SENDER', mail_username)
    mail_timeout = current_app.config.get('MAIL_TIMEOUT', 30)
    mail_provider = current_app.config.get('MAIL_PROVIDER', 'gmail')
    
    # Security check - never log passwords
    if not mail_username or not mail_password:
        logger.error("Email credentials not configured in environment variables")
        return False
    
    # Skip placeholder emails
    if 'your-email' in mail_username.lower() or 'your-gmail' in mail_username.lower() or 'example' in mail_username.lower():
        logger.warning("Email not configured - using placeholder values")
        return False
    
    # Validate email format
    if not '@' in to or not '.' in to.split('@')[1]:
        logger.error(f"Invalid recipient email format: {to}")
        return False
    
    # Create message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = mail_sender
    msg['To'] = to
    msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')
    
    # Add body parts
    text_part = MIMEText(body, 'plain', 'utf-8')
    msg.attach(text_part)
    
    if html_body:
        html_part = MIMEText(html_body, 'html', 'utf-8')
        msg.attach(html_part)
    
    # Attempt to send with retry logic
    for attempt in range(retries):
        try:
            logger.info(f"Attempting to send email to {to} (attempt {attempt + 1}/{retries})")
            
            # Connect to SMTP server
            with smtplib.SMTP(mail_server, mail_port, timeout=mail_timeout) as server:
                # Enable debug logging for development
                if current_app.config.get('DEBUG', False):
                    server.set_debuglevel(1)
                
                # Setup encryption
                if mail_use_ssl:
                    server.starttls()
                elif mail_use_tls:
                    server.starttls()
                
                # Login with timeout
                server.login(mail_username, mail_password)
                
                # Send message
                server.send_message(msg)
                
                logger.info(f"Email sent successfully to {to}")
                return True
                
        except smtplib.SMTPAuthenticationError as e:
            logger.error(f"SMTP Authentication failed for {mail_username}: {e}")
            # Don't retry authentication errors
            return False
            
        except smtplib.SMTPRecipientsRefused as e:
            logger.error(f"All recipients refused: {e}")
            # Don't retry recipient errors
            return False
            
        except smtplib.SMTPServerDisconnected as e:
            logger.warning(f"SMTP server disconnected (attempt {attempt + 1}): {e}")
            if attempt < retries - 1:
                time.sleep(current_app.config.get('MAIL_RETRY_DELAY', 5))
                continue
            return False
            
        except smtplib.SMTPException as e:
            logger.error(f"SMTP error (attempt {attempt + 1}): {e}")
            if attempt < retries - 1:
                time.sleep(current_app.config.get('MAIL_RETRY_DELAY', 5))
                continue
            return False
            
        except Exception as e:
            logger.error(f"Unexpected error sending email (attempt {attempt + 1}): {e}")
            if attempt < retries - 1:
                time.sleep(current_app.config.get('MAIL_RETRY_DELAY', 5))
                continue
            return False
    
    logger.error(f"Failed to send email after {retries} attempts")
    return False

def send_sms(phone, message):
    """Send SMS using Fast2SMS API"""
    try:
        api_key = current_app.config.get('FAST2SMS_API_KEY')
        
        if not api_key:
            print("SMS API key not configured")
            return False
        
        # Fast2SMS API endpoint
        url = "https://www.fast2sms.com/dev/bulkV2"
        
        # Prepare payload
        payload = {
            'authorization': api_key,
            'route': 'v3',
            'sender_id': 'SHOPSERV',
            'message': message,
            'language': 'english',
            'flash': 0,
            'numbers': phone
        }
        
        headers = {
            'authorization': api_key,
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cache-Control': 'no-cache'
        }
        
        response = requests.post(url, data=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if result.get('return'):
                print(f"SMS sent successfully to {phone}")
                return True
        
        print(f"SMS error: {response.text}")
        return False
    except Exception as e:
        print(f"SMS error: {e}")
        return False

def generate_order_number():
    """Generate unique order number"""
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    random_suffix = secrets.token_hex(3).upper()
    return f"ORD-{timestamp}-{random_suffix}"

def format_currency(amount):
    """Format amount as currency"""
    return f"₹{amount:,.2f}"

def create_notification(user_id, message):
    """Create notification for user"""
    from app.models.models import Notification
    notification = Notification(user_id=user_id, message=message)
    db.session.add(notification)
    db.session.commit()

def generate_qr_code(upi_id, amount, order_number):
    """Generate UPI QR code for payment"""
    # UPI payment string format
    upi_string = f"upi://pay?pa={upi_id}&pn=SHOPSERV&am={amount}&cu=INR&tn=Order {order_number}"
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(upi_string)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_str}"

def send_otp_email(user_email, user_name, otp_code, expiry_minutes=10):
    """Send OTP email with professional HTML template"""
    from flask import render_template
    
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
