#!/usr/bin/env python3
"""
SHOP_SERV - Local Shop E-commerce Platform

This is the main entry point for the SHOP_SERV application.
"""
import os
from app import create_app

# Create the Flask application
app = create_app(os.getenv('FLASK_ENV') or 'default')

if __name__ == '__main__':
    # Run the application
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
