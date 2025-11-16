import os
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from datetime import datetime
import stripe

from config import Config
from app.models.models import db, User, Shop, Product, Service, CartItem, ServiceCartItem, Order, OrderItem, ServiceOrderItem, Notification
from forms import (RegistrationForm, LoginForm, ForgotPasswordForm, VerifyOTPForm, 
                   ResetPasswordForm, ProfileForm, ShopForm, ProductForm, ServiceForm, CheckoutForm)
from utils import (save_image, delete_image, create_otp, verify_otp, send_email, send_sms,
                   generate_order_number, create_notification, generate_qr_code)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Configure Stripe
if app.config['STRIPE_SECRET_KEY']:
    stripe.api_key = app.config['STRIPE_SECRET_KEY']

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create upload folders
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'products'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'shops'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'services'), exist_ok=True)

# ==================== PUBLIC ROUTES ====================

@app.route('/')
def index():
    products = Product.query.filter_by(is_active=True).order_by(Product.created_at.desc()).limit(12).all()
    return render_template('index.html', products=products)

@app.route('/shops')
def shops():
    shops_list = Shop.query.filter_by(is_active=True, is_approved=True).all()
    return render_template('shops.html', shops=shops_list)

@app.route('/products')
def products():
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    query = Product.query.filter_by(is_active=True)
    
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    if category:
        query = query.filter_by(category=category)
        
    products = query.order_by(Product.created_at.desc()).all()
    return render_template('products.html', products=products, search=search, category=category)

# ... rest of the file remains the same ...
