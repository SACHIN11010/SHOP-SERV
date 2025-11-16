# Create email directory and OTP template
import os

# Create email directory
templates_dir = 'templates'
email_dir = os.path.join(templates_dir, 'email')

if not os.path.exists(email_dir):
    os.makedirs(email_dir)
    print(f"Created directory: {email_dir}")
else:
    print(f"Directory already exists: {email_dir}")

# Create professional HTML OTP template
otp_template_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OTP Verification - SHOP&SERV</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
        }
        
        .email-container {
            max-width: 600px;
            margin: 0 auto;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        }
        
        .header {
            background: rgba(255, 255, 255, 0.1);
            padding: 40px 30px;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        
        .logo {
            font-size: 32px;
            font-weight: bold;
            color: white;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .tagline {
            color: rgba(255, 255, 255, 0.9);
            font-size: 16px;
            font-weight: 300;
        }
        
        .content {
            background: white;
            padding: 40px 30px;
            text-align: center;
        }
        
        .greeting {
            font-size: 24px;
            color: #333;
            margin-bottom: 20px;
            font-weight: 600;
        }
        
        .message {
            font-size: 16px;
            color: #666;
            margin-bottom: 30px;
            line-height: 1.6;
        }
        
        .otp-container {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            border-radius: 15px;
            padding: 30px;
            margin: 30px 0;
            box-shadow: 0 10px 30px rgba(245, 87, 108, 0.3);
        }
        
        .otp-label {
            color: white;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 15px;
            font-weight: 600;
        }
        
        .otp-code {
            font-size: 48px;
            font-weight: bold;
            color: white;
            letter-spacing: 8px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            font-family: 'Courier New', monospace;
            margin-bottom: 10px;
        }
        
        .otp-expiry {
            color: rgba(255, 255, 255, 0.9);
            font-size: 14px;
            font-style: italic;
        }
        
        .security-note {
            background: #f8f9fa;
            border-left: 4px solid #28a745;
            padding: 20px;
            margin: 30px 0;
            border-radius: 0 10px 10px 0;
        }
        
        .security-note h4 {
            color: #28a745;
            margin-bottom: 10px;
            font-size: 16px;
        }
        
        .security-note p {
            color: #666;
            font-size: 14px;
            line-height: 1.5;
        }
        
        .footer {
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            border-top: 1px solid #e9ecef;
        }
        
        .footer-text {
            color: #6c757d;
            font-size: 14px;
            margin-bottom: 15px;
        }
        
        .footer-links {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
        }
        
        .footer-links a {
            color: #667eea;
            text-decoration: none;
            font-size: 14px;
            transition: color 0.3s ease;
        }
        
        .footer-links a:hover {
            color: #764ba2;
            text-decoration: underline;
        }
        
        .social-icons {
            display: flex;
            justify-content: center;
            gap: 15px;
            margin-top: 20px;
        }
        
        .social-icon {
            width: 36px;
            height: 36px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            text-decoration: none;
            font-size: 16px;
            transition: transform 0.3s ease;
        }
        
        .social-icon:hover {
            transform: translateY(-3px);
        }
        
        .button {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border-radius: 25px;
            text-decoration: none;
            font-weight: 600;
            margin: 20px 0;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        @media (max-width: 600px) {
            .email-container {
                margin: 10px;
                border-radius: 15px;
            }
            
            .header {
                padding: 30px 20px;
            }
            
            .content {
                padding: 30px 20px;
            }
            
            .otp-code {
                font-size: 36px;
                letter-spacing: 6px;
            }
            
            .footer-links {
                flex-direction: column;
                gap: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="email-container">
        <!-- Header Section -->
        <div class="header">
            <div class="logo">SHOP&SERV</div>
            <div class="tagline">Your Trusted Shopping & Service Partner</div>
        </div>
        
        <!-- Main Content -->
        <div class="content">
            <h1 class="greeting">Hello {{ user_name }}!</h1>
            
            <p class="message">
                We received a request to verify your email address for your SHOP&SERV account. 
                Use the verification code below to complete the process.
            </p>
            
            <!-- OTP Code Section -->
            <div class="otp-container">
                <div class="otp-label">Your Verification Code</div>
                <div class="otp-code">{{ otp_code }}</div>
                <div class="otp-expiry">This code will expire in {{ expiry_minutes }} minutes</div>
            </div>
            
            <!-- Security Note -->
            <div class="security-note">
                <h4>🔒 Security Notice</h4>
                <p>
                    Never share this verification code with anyone. Our team will never ask for your 
                    verification code via email, phone, or any other method. If you didn't request this 
                    code, please ignore this email or contact our support team immediately.
                </p>
            </div>
            
            <!-- Action Button -->
            <a href="{{ verification_url }}" class="button">Verify Email Now</a>
            
            <p class="message">
                If the button above doesn't work, you can copy and paste the verification code 
                directly into the application.
            </p>
        </div>
        
        <!-- Footer Section -->
        <div class="footer">
            <p class="footer-text">
                This email was sent to {{ user_email }} because you requested a verification code 
                for your SHOP&SERV account.
            </p>
            
            <div class="footer-links">
                <a href="{{ website_url }}">Visit Our Website</a>
                <a href="{{ support_url }}">Contact Support</a>
                <a href="{{ privacy_url }}">Privacy Policy</a>
            </div>
            
            <div class="social-icons">
                <a href="{{ facebook_url }}" class="social-icon">f</a>
                <a href="{{ twitter_url }}" class="social-icon">t</a>
                <a href="{{ instagram_url }}" class="social-icon">i</a>
            </div>
            
            <p class="footer-text" style="margin-top: 20px;">
                © 2024 SHOP&SERV. All rights reserved.
            </p>
        </div>
    </div>
</body>
</html>'''

# Write the template file
template_file = os.path.join(email_dir, 'otp_template.html')
with open(template_file, 'w', encoding='utf-8') as f:
    f.write(otp_template_content)

print(f"Created template file: {template_file}")
print("\nProfessional HTML OTP email template created successfully!")
print("\nTemplate features:")
print("- Beautiful gradient design with SHOP&SERV branding")
print("- Large, clear OTP code display")
print("- Security notices and warnings")
print("- Mobile-responsive design")
print("- Professional footer with links")
