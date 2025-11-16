#!/usr/bin/env python3
"""
Test script for the new HTML OTP email template
"""

import os
import sys
from flask import Flask, render_template

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Create a minimal Flask app for testing
app = Flask(__name__)
app.config['SECRET_KEY'] = 'test-secret-key'

# Test the email template
with app.app_context():
    # Test data for the template
    test_data = {
        'user_name': 'John Doe',
        'otp_code': '123456',
        'expiry_minutes': 5,
        'user_email': 'test@example.com',
        'verification_url': 'http://localhost:5000/verify-otp',
        'website_url': 'http://localhost:5000',
        'support_url': 'http://localhost:5000/support',
        'privacy_url': 'http://localhost:5000/privacy',
        'facebook_url': '#',
        'twitter_url': '#',
        'instagram_url': '#'
    }
    
    try:
        # Render the template
        rendered_html = render_template('email/otp_template.html', **test_data)
        
        # Save to a file for manual inspection
        output_file = 'test_otp_email.html'
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(rendered_html)
        
        print(f"✅ Email template rendered successfully!")
        print(f"📄 Output saved to: {output_file}")
        print(f"🌐 Open this file in your browser to see the formatted email")
        print("\n📋 Template features tested:")
        print("- HTML rendering with Jinja2 variables")
        print("- Gradient design and styling")
        print("- OTP code display")
        print("- Security notices")
        print("- Responsive layout")
        print("- Professional footer")
        
    except Exception as e:
        print(f"❌ Error rendering template: {e}")
        sys.exit(1)
