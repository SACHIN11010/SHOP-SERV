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
    categories = db.session.query(Product.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]
    
    return render_template('products.html', products=products, categories=categories, 
                         search=search, category=category)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/services')
def services():
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    query = Service.query.filter_by(is_active=True)
    
    if search:
        query = query.filter(Service.name.ilike(f'%{search}%'))
    if category:
        query = query.filter_by(category=category)
    
    services = query.order_by(Service.created_at.desc()).all()
    categories = db.session.query(Service.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]
    
    return render_template('services.html', services=services, categories=categories, 
                         search=search, category=category)

@app.route('/shops')
def shops():
    search = request.args.get('search', '')
    city = request.args.get('city', '')
    service_type = request.args.get('service_type', '')
    
    query = Shop.query.filter_by(is_active=True, is_approved=True)
    
    if search:
        query = query.filter(Shop.name.ilike(f'%{search}%'))
    if city:
        query = query.filter(Shop.city.ilike(f'%{city}%'))
    if service_type:
        query = query.filter_by(service_type=service_type)
    
    shops = query.order_by(Shop.created_at.desc()).all()
    
    # Get unique cities and service types for filters
    cities = db.session.query(Shop.city).distinct().all()
    cities = [c[0] for c in cities if c[0]]
    
    service_types = db.session.query(Shop.service_type).distinct().all()
    service_types = [s[0] for s in service_types if s[0]]
    
    return render_template('shops.html', shops=shops, cities=cities, service_types=service_types,
                         search=search, city=city, service_type=service_type)

@app.route('/service/<int:service_id>')
def service_detail(service_id):
    service = Service.query.get_or_404(service_id)
    return render_template('service_detail.html', service=service)

@app.route('/shop/<int:shop_id>')
def shop_detail(shop_id):
    shop = Shop.query.get_or_404(shop_id)
    # Get shop's services
    services = Service.query.filter_by(shop_id=shop_id, is_active=True).all()
    return render_template('shop_detail.html', shop=shop, services=services)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data.lower(),
            full_name=form.full_name.data,
            phone=form.phone.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        try:
            # Check for static admin credentials
            if form.email.data.lower() == 'admin' and form.password.data == 'ADMIN123':
                # Find or create admin user
                admin = User.query.filter_by(role='admin').first()
                if not admin:
                    admin = User.query.filter_by(email='admin@shopserv.com').first()
                if admin and admin.check_password(form.password.data):
                    login_user(admin)
                    return redirect(url_for('admin_dashboard'))
            
            # Regular user login
            user = User.query.filter_by(email=form.email.data.lower()).first()
            
            if user and user.check_password(form.password.data):
                if not user.is_active:
                    flash('Your account has been disabled. Please contact support.', 'danger')
                    return redirect(url_for('login'))
                
                login_user(user, remember=True)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password.', 'danger')
        except Exception as e:
            app.logger.error(f'Login error: {str(e)}')
            flash('An error occurred during login. Please try again.', 'danger')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        
        if user:
            otp_code = create_otp(user.email)
            
            # Try to send OTP via email
            email_sent = False
            sms_sent = False
            
            subject = "Password Reset OTP - SHOP&SERV"
            
            # Render HTML email template
            html_body = render_template('email/otp_template.html', 
                                       user_name=user.full_name or user.email.split('@')[0],
                                       otp_code=otp_code,
                                       expiry_minutes=5,
                                       user_email=user.email,
                                       verification_url=url_for('verify_otp_route', _external=True),
                                       website_url=url_for('index', _external=True),
                                       support_url=url_for('index', _external=True),
                                       privacy_url=url_for('index', _external=True),
                                       facebook_url="#",
                                       twitter_url="#",
                                       instagram_url="#")
            
            # Plain text fallback for email clients that don't support HTML
            text_body = f"""
Password Reset Request - SHOP&SERV

Hello {user.full_name or user.email.split('@')[0]},

We received a request to reset your password for your SHOP&SERV account.

Your OTP code is: {otp_code}
This code will expire in 5 minutes.

If you didn't request this, please ignore this email.

For security reasons, never share this code with anyone.

© 2024 SHOP&SERV. All rights reserved.
            """
            
            email_sent = send_email(user.email, subject, text_body, html_body)
            
            # Try to send OTP via SMS if user has phone
            if user.phone:
                sms_message = f"Your SHOP&SERV password reset OTP is: {otp_code}. Valid for 5 minutes."
                sms_sent = send_sms(user.phone, sms_message)
            
            # Show appropriate message
            if email_sent or sms_sent:
                session['reset_email'] = user.email
                if email_sent and sms_sent:
                    flash(f'OTP sent to your email ({user.email}) and mobile ({user.phone}). Please check.', 'success')
                elif email_sent:
                    flash(f'OTP sent to your email ({user.email}). Please check your inbox.', 'success')
                elif sms_sent:
                    flash(f'OTP sent to your mobile ({user.phone}). Please check your messages.', 'success')
                return redirect(url_for('verify_otp_route'))
            else:
                # Email/SMS not configured properly
                flash('Email service is not configured. Please contact administrator to set up email credentials.', 'danger')
        else:
            # Don't reveal if email exists
            flash('If the email exists, an OTP has been sent.', 'info')
    
    return render_template('forgot_password.html', form=form)

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp_route():
    if 'reset_email' not in session:
        return redirect(url_for('forgot_password'))
    
    form = VerifyOTPForm()
    if form.validate_on_submit():
        if verify_otp(session['reset_email'], form.otp.data):
            session['otp_verified'] = True
            flash('OTP verified! Please set your new password.', 'success')
            return redirect(url_for('reset_password'))
        else:
            flash('Invalid or expired OTP. Please try again.', 'danger')
    
    return render_template('verify_otp.html', form=form)

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if 'reset_email' not in session or not session.get('otp_verified'):
        return redirect(url_for('forgot_password'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=session['reset_email']).first()
        if user:
            user.set_password(form.password.data)
            db.session.commit()
            
            # Clear session
            session.pop('reset_email', None)
            session.pop('otp_verified', None)
            
            flash('Password reset successful! Please log in with your new password.', 'success')
            return redirect(url_for('login'))
    
    return render_template('reset_password.html', form=form)

# ==================== DASHBOARD ROUTES ====================

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif current_user.role == 'shopowner':
        return redirect(url_for('shop_dashboard'))
    else:
        return redirect(url_for('customer_dashboard'))

@app.route('/customer/dashboard')
@login_required
def customer_dashboard():
    if current_user.role != 'customer':
        return redirect(url_for('dashboard'))
    
    orders = Order.query.filter_by(customer_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('customer/dashboard.html', orders=orders)

@app.route('/customer/profile', methods=['GET', 'POST'])
@login_required
def customer_profile():
    if current_user.role != 'customer':
        return redirect(url_for('dashboard'))
    
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.full_name = form.full_name.data
        current_user.phone = form.phone.data
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('customer_profile'))
    
    return render_template('customer/profile.html', form=form)

# ==================== CART & CHECKOUT ====================

@app.route('/cart')
@login_required
def cart():
    if current_user.role != 'customer':
        flash('Only customers can access the cart.', 'warning')
        return redirect(url_for('dashboard'))
    
    cart_items = CartItem.query.filter_by(customer_id=current_user.id).all()
    service_cart_items = ServiceCartItem.query.filter_by(customer_id=current_user.id).all()
    
    total = sum(item.product.price * item.quantity for item in cart_items if item.product.is_active)
    total += sum(item.service.price * item.quantity for item in service_cart_items if item.service.is_active)
    
    return render_template('cart.html', cart_items=cart_items, service_cart_items=service_cart_items, total=total)

@app.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    if current_user.role != 'customer':
        return jsonify({'success': False, 'message': 'Only customers can add to cart'}), 403
    
    product = Product.query.get_or_404(product_id)
    
    if not product.is_active or product.stock < 1:
        return jsonify({'success': False, 'message': 'Product not available'}), 400
    
    cart_item = CartItem.query.filter_by(customer_id=current_user.id, product_id=product_id).first()
    
    if cart_item:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
        else:
            return jsonify({'success': False, 'message': 'Not enough stock'}), 400
    else:
        cart_item = CartItem(customer_id=current_user.id, product_id=product_id, quantity=1)
        db.session.add(cart_item)
    
    db.session.commit()
    
    cart_count = CartItem.query.filter_by(customer_id=current_user.id).count()
    return jsonify({'success': True, 'message': 'Added to cart', 'cart_count': cart_count})

@app.route('/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    
    if cart_item.customer_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    quantity = request.json.get('quantity', 1)
    
    if quantity < 1:
        return jsonify({'success': False, 'message': 'Invalid quantity'}), 400
    
    if quantity > cart_item.product.stock:
        return jsonify({'success': False, 'message': 'Not enough stock'}), 400
    
    cart_item.quantity = quantity
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Cart updated'})

@app.route('/cart/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_cart(item_id):
    cart_item = CartItem.query.get_or_404(item_id)
    
    if cart_item.customer_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Item removed'})

@app.route('/cart/add-service/<int:service_id>', methods=['POST'])
@login_required
def add_service_to_cart(service_id):
    if current_user.role != 'customer':
        return jsonify({'success': False, 'message': 'Only customers can add to cart'}), 403
    
    service = Service.query.get_or_404(service_id)
    
    if not service.is_active:
        return jsonify({'success': False, 'message': 'Service not available'}), 400
    
    cart_item = ServiceCartItem.query.filter_by(customer_id=current_user.id, service_id=service_id).first()
    
    if cart_item:
        cart_item.quantity += 1
    else:
        cart_item = ServiceCartItem(customer_id=current_user.id, service_id=service_id, quantity=1)
        db.session.add(cart_item)
    
    db.session.commit()
    
    cart_count = CartItem.query.filter_by(customer_id=current_user.id).count()
    cart_count += ServiceCartItem.query.filter_by(customer_id=current_user.id).count()
    return jsonify({'success': True, 'message': 'Added to cart', 'cart_count': cart_count})

@app.route('/cart/update-service/<int:item_id>', methods=['POST'])
@login_required
def update_service_cart(item_id):
    cart_item = ServiceCartItem.query.get_or_404(item_id)
    
    if cart_item.customer_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    quantity = request.json.get('quantity', 1)
    
    if quantity < 1:
        return jsonify({'success': False, 'message': 'Invalid quantity'}), 400
    
    cart_item.quantity = quantity
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Cart updated'})

@app.route('/cart/remove-service/<int:item_id>', methods=['POST'])
@login_required
def remove_service_from_cart(item_id):
    cart_item = ServiceCartItem.query.get_or_404(item_id)
    
    if cart_item.customer_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    db.session.delete(cart_item)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Service removed'})

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    if current_user.role != 'customer':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'success': False, 'error': 'Only customers can checkout.'}), 403
        flash('Only customers can checkout.', 'warning')
        return redirect(url_for('dashboard'))
    
    # Get cart items with active products
    cart_items = CartItem.query.join(Product).filter(
        CartItem.customer_id == current_user.id,
        Product.is_active == True
    ).all()
    
    # Get service cart items with active services
    service_cart_items = ServiceCartItem.query.join(Service).filter(
        ServiceCartItem.customer_id == current_user.id,
        Service.is_active == True
    ).all()
    
    # For AJAX requests, we'll return JSON responses
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    def json_response(success, message=None, redirect_url=None, error=None):
        response = {'success': success}
        if message:
            response['message'] = message
        if redirect_url:
            response['redirect'] = redirect_url
        if error:
            response['error'] = error
        return jsonify(response)
    
    # Check if cart is empty
    if not cart_items and not service_cart_items:
        if is_ajax:
            return json_response(False, redirect=url_for('cart')), 400
        flash('Your cart is empty.', 'warning')
        return redirect(url_for('cart'))
    
    # Calculate total and check stock availability
    total = 0
    out_of_stock = False
    
    for item in cart_items:
        if item.quantity > item.product.stock:
            out_of_stock = True
            item.quantity = item.product.stock
    if request.method == 'GET':
        # Show checkout form
        cart_items = CartItem.query.filter_by(customer_id=current_user.id).all()
        service_cart_items = ServiceCartItem.query.filter_by(customer_id=current_user.id).all()
        
        if not cart_items and not service_cart_items:
            if is_ajax:
                return jsonify({'success': False, 'redirect': url_for('cart')}), 400
            flash('Your cart is empty.', 'warning')
            return redirect(url_for('cart'))
            
        # Calculate totals
        total = 0
        for item in cart_items:
            total += item.product.price * item.quantity
        for item in service_cart_items:
            total += item.service.price
            
        if is_ajax:
            return jsonify({
                'success': True,
                'html': render_template('_checkout_content.html',  # We'll create this partial
                                     cart_items=cart_items,
                                     service_cart_items=service_cart_items,
                                     total=total)
            })
            
        return render_template('checkout.html', 
                            cart_items=cart_items, 
                            service_cart_items=service_cart_items,
                            total=total)
    
    # Handle POST request
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        try:
            # Get form data
            if request.is_json:
                data = request.get_json()
                payment_method = data.get('payment_method')
                shipping_address = data.get('shipping_address')
                shipping_city = data.get('shipping_city', '')
                shipping_state = data.get('shipping_state', '')
                shipping_zip = data.get('shipping_zip', '')
                shipping_phone = data.get('shipping_phone', '')
                terms_accepted = data.get('terms_accepted', 'false').lower() == 'true'
                notes = data.get('notes', '')
            else:
                payment_method = request.form.get('payment_method')
                shipping_address = request.form.get('shipping_address')
                shipping_city = request.form.get('shipping_city', '')
                shipping_state = request.form.get('shipping_state', '')
                shipping_zip = request.form.get('shipping_zip', '')
                shipping_phone = request.form.get('shipping_phone', '')
                terms_accepted = request.form.get('terms_accepted', 'false').lower() == 'true'
                notes = request.form.get('notes', '')
            
            # Debug log
            app.logger.debug(f'Checkout data - terms_accepted: {terms_accepted}, payment_method: {payment_method}, shipping_address: {shipping_address}')
            
            # Set default values for demo
            shipping_city = shipping_city or 'Demo City'
            shipping_state = shipping_state or 'Demo State'
            shipping_zip = shipping_zip or '12345'
            
            # Validate required fields
            required_fields = {
                'Payment Method': payment_method,
                'Shipping Address': shipping_address,
                'Phone Number': shipping_phone
            }
            
            missing_fields = [field for field, value in required_fields.items() if not value]
            if missing_fields:
                error_msg = f'Missing required fields: {", ".join(missing_fields)}'
                app.logger.warning(f'Validation failed: {error_msg}')
                if is_ajax:
                    return jsonify({'success': False, 'error': error_msg}), 400
                flash(error_msg, 'danger')
                return redirect(url_for('checkout'))
            
            # Validate terms acceptance
            if not terms_accepted:
                error_msg = 'You must accept the terms and conditions to proceed.'
                if is_ajax:
                    return jsonify({'success': False, 'error': error_msg}), 400
                flash(error_msg, 'danger')
                return redirect(url_for('checkout'))
            
            # Check if cart is not empty
            if not cart_items and not service_cart_items:
                error_msg = 'Your cart is empty.'
                if is_ajax:
                    return jsonify({'success': False, 'error': error_msg}), 400
                flash(error_msg, 'warning')
                return redirect(url_for('cart'))
                
            # Check product availability and stock
            for item in cart_items:
                if not item.product.is_active or item.product.stock < item.quantity:
                    error_msg = f'Sorry, {item.product.name} is not available in the requested quantity.'
                    if is_ajax:
                        return jsonify({'success': False, 'error': error_msg}), 400
                    flash(error_msg, 'danger')
                    return redirect(url_for('cart'))
            
            # Validate terms acceptance
            if not terms_accepted:
                error_msg = 'You must accept the terms and conditions to proceed.'
                if is_ajax:
                    return json_response(False, error=error_msg)
                flash(error_msg, 'danger')
                return redirect(url_for('checkout'))
            
            # Verify stock before creating order
            for item in cart_items:
                if item.quantity > item.product.stock:
                    error_msg = f'Sorry, there are only {item.product.stock} units of {item.product.name} available.'
                    app.logger.warning(error_msg)
                    if is_ajax:
                        return jsonify({'success': False, 'error': error_msg}), 400
                    flash(error_msg, 'danger')
                    return redirect(url_for('cart'))
            
            # Combine address components
            full_address = f"{shipping_address}\n{shipping_city}, {shipping_state} {shipping_zip}"
            
            try:
                # Start a transaction
                db.session.begin_nested()
                
                # Generate order number
                order_number = generate_order_number()
                
                # Create order
                order = Order(
                    order_number=order_number,
                    customer_id=current_user.id,
                    total_amount=total,
                    payment_method=payment_method,
                    shipping_address=full_address.strip(),
                    shipping_phone=shipping_phone,
                    notes=notes,
                    status='pending_payment',
                    terms_accepted=True,
                    created_at=datetime.utcnow()
                )
                db.session.add(order)
                db.session.flush()  # Get the order ID
                
                # Add order items
                for item in cart_items:
                    # Create order item
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=item.product_id,
                        quantity=item.quantity,
                        price=item.product.price,
                        total=item.product.price * item.quantity
                    )
                    db.session.add(order_item)
                    
                    # Update product stock
                    item.product.stock -= item.quantity
                
                # Clear the cart after successful order
                CartItem.query.filter_by(customer_id=current_user.id).delete()
                
                # Commit the transaction
                db.session.commit()
                
                # Log successful order
                app.logger.info(f'Order {order.order_number} created successfully for user {current_user.id}')
                
                # Process payment based on method
                if payment_method == 'online':
                    # For demo, just mark as paid since we're showing QR code directly
                    order.status = 'paid'
                    order.payment_method = 'online'
                    db.session.commit()
                    
                    if is_ajax:
                        return jsonify({
                            'success': True,
                            'redirect': url_for('order_detail', order_id=order.id),
                            'message': 'Order placed successfully! Thank you for your payment.'
                        })
                    return redirect(url_for('order_detail', order_id=order.id))
                else:
                    # For COD, mark as pending
                    order.status = 'pending'
                    db.session.commit()
                    
                    if is_ajax:
                        return jsonify({
                            'success': True,
                            'redirect': url_for('order_detail', order_id=order.id),
                            'message': 'Order placed successfully! We will contact you for payment on delivery.'
                        })
                    return redirect(url_for('order_detail', order_id=order.id))
                
            except Exception as e:
                db.session.rollback()
                app.logger.error(f'Error creating order: {str(e)}')
                error_msg = 'An error occurred while processing your order. Please try again.'
                if is_ajax:
                    return json_response(False, error=error_msg)
                flash(error_msg, 'danger')
                return redirect(url_for('checkout'))
            
            # Create order items for products
            for item in cart_items:
                if not item.product.is_active or item.product.stock < item.quantity:
                    db.session.rollback()
                    error_msg = f'Sorry, {item.product.name} is no longer available in the requested quantity.'
                    app.logger.warning(error_msg)
                    if is_ajax:
                        return jsonify({'success': False, 'error': error_msg}), 400
                    flash(error_msg, 'danger')
                    return redirect(url_for('cart'))
                
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    shop_id=item.product.shop_id,
                    quantity=item.quantity,
                    price=item.product.price,
                    status='pending'
                )
                db.session.add(order_item)
                
                # Update stock
                item.product.stock -= item.quantity
            
            # Create order items for services
            for item in service_cart_items:
                if not item.service.is_active:
                    db.session.rollback()
                    error_msg = f'Sorry, {item.service.name} is no longer available.'
                    if is_ajax:
                        return json_response(False, error=error_msg)
                    flash(error_msg, 'danger')
                    return redirect(url_for('cart'))
                
                service_order_item = ServiceOrderItem(
                    order_id=order.id,
                    service_id=item.service_id,
                    shop_id=item.service.shop_id,
                    quantity=item.quantity,
                    price=item.service.price,
                    status='pending'
                )
                db.session.add(service_order_item)
            
            try:
                # Clear cart
                CartItem.query.filter_by(customer_id=current_user.id).delete()
                ServiceCartItem.query.filter_by(customer_id=current_user.id).delete()
                
                db.session.commit()
                
                # Store order ID for payment
                session['pending_order_id'] = order.id
                
                # Handle response based on payment method
                if payment_method == 'online':
                    redirect_url = url_for('payment', order_id=order.id)
                    if is_ajax:
                        return json_response(True, message='Order created successfully', redirect=redirect_url)
                    return redirect(redirect_url)
                elif payment_method == 'cod':
                    # For Cash on Delivery, mark as paid and redirect to success
                    order.payment_status = 'pending'
                    order.status = 'processing'
                    db.session.commit()
                    
                    # Send order confirmation email
                    try:
                        send_order_confirmation_email(order, current_user)
                    except Exception as e:
                        app.logger.error(f'Error sending order confirmation email: {str(e)}')
                    
                    redirect_url = url_for('order_detail', order_id=order.id)
                    if is_ajax:
                        return json_response(True, message='Your order has been placed successfully!', redirect=redirect_url)
                    flash('Your order has been placed successfully!', 'success')
                    return redirect(redirect_url)
                else:
                    # For other payment methods, redirect to payment page
                    redirect_url = url_for('payment', order_id=order.id)
                    if is_ajax:
                        return json_response(True, message='Redirecting to payment...', redirect=redirect_url)
                    return redirect(redirect_url)
                
            except Exception as e:
                db.session.rollback()
                app.logger.error(f'Error during order processing: {str(e)}')
                error_msg = 'An error occurred while processing your order. Please try again.'
                if is_ajax:
                    return json_response(False, error=error_msg)
                flash(error_msg, 'danger')
                return redirect(url_for('checkout'))
                
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error during checkout: {str(e)}')
            error_msg = 'An error occurred while processing your order. Please try again.'
            if is_ajax:
                return json_response(False, error=error_msg)
            flash(error_msg, 'danger')
            return redirect(url_for('checkout'))
    
    if order.customer_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard'))
    
    if order.payment_status == 'completed':
        flash('This order has already been paid.', 'info')
        return redirect(url_for('order_detail', order_id=order.id))
    
    # Handle COD - immediate confirmation
    if order.payment_method == 'cod':
        order.payment_status = 'pending'
        order.status = 'confirmed'
        db.session.commit()
        
        # Notify shop owners
        for item in order.items:
            create_notification(
                item.shop.owner_id,
                f'New COD order #{order.order_number} received for {item.product.name}'
            )
        for item in order.service_items:
            create_notification(
                item.shop.owner_id,
                f'New COD order #{order.order_number} received for {item.service.name}'
            )
        
        flash('Order placed successfully! Pay cash on delivery.', 'success')
        return redirect(url_for('order_detail', order_id=order.id))
    
    # Handle QR Code payment
    if order.payment_method == 'qr':
        qr_code = generate_qr_code(
            app.config['UPI_ID'],
            order.total_amount,
            order.order_number
        )
        return render_template('payment_qr.html', order=order, qr_code=qr_code)
    
    # Handle Stripe payment
    stripe_public_key = app.config['STRIPE_PUBLIC_KEY']
    return render_template('payment.html', order=order, stripe_public_key=stripe_public_key)

@app.route('/create-payment-intent', methods=['POST'])
@login_required
def create_payment_intent():
    try:
        data = request.json
        order_id = data.get('order_id')
        
        order = Order.query.get_or_404(order_id)
        
        if order.customer_id != current_user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Create Stripe payment intent
        intent = stripe.PaymentIntent.create(
            amount=int(order.total_amount * 100),  # Amount in paise (100 paise = 1 INR)
            currency='inr',
            metadata={'order_id': order.id, 'order_number': order.order_number}
        )
        
        order.payment_intent_id = intent.id
        db.session.commit()
        
        return jsonify({'clientSecret': intent.client_secret})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/payment-success/<int:order_id>')
@login_required
def payment_success(order_id):
    order = Order.query.get_or_404(order_id)
    
    if order.customer_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard'))
    
    # Update order status
    order.payment_status = 'completed'
    order.status = 'confirmed'
    db.session.commit()
    
    # Notify shop owners
    for item in order.items:
        create_notification(
            item.shop.owner_id,
            f'New order #{order.order_number} received for {item.product.name}'
        )
    for item in order.service_items:
        create_notification(
            item.shop.owner_id,
            f'New order #{order.order_number} received for {item.service.name}'
        )
    
    flash('Payment successful! Your order has been confirmed.', 'success')
    return redirect(url_for('order_detail', order_id=order.id))

@app.route('/confirm-qr-payment/<int:order_id>', methods=['POST'])
@login_required
def confirm_qr_payment(order_id):
    order = Order.query.get_or_404(order_id)
    
    if order.customer_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Mark payment as completed (in production, verify with payment gateway)
    order.payment_status = 'completed'
    order.status = 'confirmed'
    db.session.commit()
    
    # Notify shop owners
    for item in order.items:
        create_notification(
            item.shop.owner_id,
            f'New QR payment order #{order.order_number} received for {item.product.name}'
        )
    for item in order.service_items:
        create_notification(
            item.shop.owner_id,
            f'New QR payment order #{order.order_number} received for {item.service.name}'
        )
    
    return jsonify({'success': True, 'message': 'Payment confirmed'})

@app.route('/cancel-order/<int:order_id>', methods=['POST'])
@login_required
def cancel_order(order_id):
    order = Order.query.get_or_404(order_id)
    
    if order.customer_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Only allow cancellation if order is pending or payment is not completed
    if order.status in ['delivered', 'cancelled']:
        return jsonify({'success': False, 'message': 'Cannot cancel this order'}), 400
    
    # Cancel the order
    order.status = 'cancelled'
    order.payment_status = 'cancelled'
    db.session.commit()
    
    # Notify shop owners
    for item in order.items:
        create_notification(
            item.shop.owner_id,
            f'Order #{order.order_number} has been cancelled by customer'
        )
    for item in order.service_items:
        create_notification(
            item.shop.owner_id,
            f'Order #{order.order_number} has been cancelled by customer'
        )
    
    return jsonify({'success': True, 'message': 'Order cancelled'})

@app.route('/check-payment-status/<int:order_id>')
@login_required
def check_payment_status(order_id):
    order = Order.query.get_or_404(order_id)
    
    if order.customer_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    return jsonify({
        'success': True,
        'payment_status': order.payment_status,
        'order_status': order.status
    })

@app.route('/order/<int:order_id>/upload_payment', methods=['GET', 'POST'])
@login_required
def upload_payment(order_id):
    order = Order.query.get_or_404(order_id)
    if order.customer_id != current_user.id:
        abort(403)
    
    if request.method == 'POST':
        if 'payment_proof' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['payment_proof']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(f"payment_{order.id}_{file.filename}")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'payments', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)
            
            # Update order with payment proof
            order.payment_proof = f"payments/{filename}"
            order.status = 'payment_received'
            db.session.commit()
            
            flash('Payment proof uploaded successfully! We will verify your payment shortly.', 'success')
            return redirect(url_for('order_detail', order_id=order.id))
    
    return render_template('upload_payment.html', order=order)

@app.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    if order.customer_id != current_user.id and current_user.role != 'admin':
        abort(403)
    return render_template('order_detail.html', order=order)

# ==================== SHOP OWNER ROUTES ====================

@app.route('/shop/dashboard')
@login_required
def shop_dashboard():
    if current_user.role != 'shopowner':
        return redirect(url_for('dashboard'))
    
    # Get the first shop for the user (assuming one-to-many relationship)
    shop = current_user.shops.first()
    if not shop:
        flash('You need to create a shop first.', 'warning')
        return redirect(url_for('create_shop'))
    
    products = Product.query.filter_by(shop_id=shop.id).all()
    orders = OrderItem.query.filter_by(shop_id=shop.id).order_by(OrderItem.id.desc()).limit(10).all()
    
    total_products = len(products)
    total_orders = OrderItem.query.filter_by(shop_id=shop.id).count()
    total_revenue = db.session.query(db.func.sum(OrderItem.price * OrderItem.quantity)).filter_by(shop_id=shop.id).scalar() or 0
    
    return render_template('shop/dashboard.html', shop=shop, products=products, orders=orders,
                         total_products=total_products, total_orders=total_orders, total_revenue=total_revenue)

@app.route('/shop/create', methods=['GET', 'POST'])
@login_required
def create_shop():
    if current_user.role != 'shopowner':
        return redirect(url_for('dashboard'))
    
    # Check if user already has a shop using the correct relationship name
    if hasattr(current_user, 'shops') and current_user.shops.first():
        flash('You already have a shop.', 'info')
        return redirect(url_for('shop_dashboard'))
    
    form = ShopForm()
    if form.validate_on_submit():
        try:
            logo_path = None
            if form.logo.data:
                logo_path = save_image(form.logo.data, 'shops')
            
            # Create the shop
            shop = Shop(
                owner_id=current_user.id,
                name=form.name.data,
                description=form.description.data,
                address=form.address.data,
                city=form.city.data,
                state=form.state.data,
                pincode=form.pincode.data,
                contact_phone=form.contact_phone.data,
                service_type=form.service_type.data,
                logo=logo_path,
                is_active=True
            )
            
            db.session.add(shop)
            db.session.commit()
            
            # Update the user's shop relationship
            if not hasattr(current_user, 'shops'):
                current_user.shops = []
            current_user.shops.append(shop)
            db.session.commit()
            
            flash('Shop created successfully!', 'success')
            return redirect(url_for('shop_dashboard'))
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error creating shop: {str(e)}')
            flash('An error occurred while creating your shop. Please try again.', 'error')
    
    return render_template('shop/create_shop.html', form=form)

@app.route('/shop/edit', methods=['GET', 'POST'])
@login_required
def edit_shop():
    if current_user.role != 'shopowner':
        return redirect(url_for('dashboard'))
    
    shop = current_user.shops.first()
    if not shop:
        flash('You need to create a shop first.', 'warning')
        return redirect(url_for('create_shop'))
    
    form = ShopForm()
    
    if request.method == 'GET':
        # Set form data from shop object
        form.name.data = shop.name
        form.delivery_charge.data = shop.delivery_charge
        form.min_order_amount.data = shop.min_order_amount
        form.is_active.data = shop.is_active
        form.upi_id.data = shop.upi_id
        form.bank_name.data = shop.bank_name
        form.account_holder_name.data = shop.account_holder_name
        form.account_number.data = shop.account_number
        form.ifsc_code.data = shop.ifsc_code
        form.preferred_payment_method.data = shop.preferred_payment_method or 'upi'
        form.address.data = shop.address
        form.city.data = shop.city
        form.state.data = shop.state
        form.pincode.data = shop.pincode
        form.contact_phone.data = shop.contact_phone
        form.contact_whatsapp.data = shop.contact_whatsapp
        form.contact_email.data = shop.contact_email
        form.opening_time.data = shop.opening_time.strftime('%H:%M') if shop.opening_time else ''
        form.closing_time.data = shop.closing_time.strftime('%H:%M') if shop.closing_time else ''
        form.is_delivery_available.data = shop.is_delivery_available
        form.is_pickup_available.data = shop.is_pickup_available
        form.is_cod_available.data = shop.is_cod_available
        form.delivery_radius_km.data = shop.delivery_radius_km
        form.delivery_charge.data = shop.delivery_charge
        form.min_order_amount.data = shop.min_order_amount
    
    if form.validate_on_submit():
        try:
            shop.name = form.name.data
            shop.description = form.description.data
            shop.service_type = form.service_type.data
            shop.address = form.address.data
            shop.city = form.city.data
            shop.state = form.state.data
            shop.pincode = form.pincode.data
            shop.contact_phone = form.contact_phone.data
            shop.contact_whatsapp = form.contact_whatsapp.data
            shop.contact_email = form.contact_email.data
            shop.opening_time = datetime.strptime(form.opening_time.data, '%H:%M').time()
            shop.closing_time = datetime.strptime(form.closing_time.data, '%H:%M').time()
            shop.is_delivery_available = form.is_delivery_available.data
            shop.is_pickup_available = form.is_pickup_available.data
            shop.is_cod_available = form.is_cod_available.data
            shop.delivery_radius_km = form.delivery_radius_km.data or 0.0
            shop.delivery_charge = form.delivery_charge.data or 0.0
            shop.min_order_amount = form.min_order_amount.data or 0.0
            shop.is_active = form.is_active.data
            
            # Save payment details
            shop.preferred_payment_method = form.preferred_payment_method.data
            shop.upi_id = form.upi_id.data
            shop.bank_name = form.bank_name.data
            shop.account_holder_name = form.account_holder_name.data
            shop.account_number = form.account_number.data
            shop.ifsc_code = form.ifsc_code.data
            
            # Handle UPI QR code upload
            if 'upi_qr_code' in request.files and request.files['upi_qr_code'].filename != '':
                qr_file = request.files['upi_qr_code']
                if qr_file and allowed_file(qr_file.filename):
                    filename = secure_filename(f"qr_{shop.id}_{qr_file.filename}")
                    qr_path = os.path.join(app.config['UPLOAD_FOLDER'], 'shops', filename)
                    qr_file.save(qr_path)
                    shop.upi_qr_code = f"shops/{filename}"
            
            # Handle QR code removal if checkbox is checked
            if 'remove_qr_code' in request.form and request.form['remove_qr_code'] == 'y':
                if shop.upi_qr_code:
                    # Delete the old QR code file if it exists
                    try:
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], shop.upi_qr_code))
                    except OSError:
                        pass
                    shop.upi_qr_code = None
            
            # Handle file upload if a new logo is provided
            if 'logo' in request.files and request.files['logo'].filename != '':
                logo_file = request.files['logo']
                if logo_file:
                    # Delete old logo if exists
                    if shop.logo:
                        try:
                            delete_image(shop.logo)
                        except Exception as e:
                            app.logger.error(f"Error deleting old logo: {str(e)}")
                    
                    # Save new logo
                    try:
                        shop.logo = save_image(logo_file, 'shops')
                        flash('Logo updated successfully!', 'success')
                    except Exception as e:
                        app.logger.error(f"Error saving new logo: {str(e)}")
                        flash('Error uploading logo. Please try again.', 'error')
                        return render_template('shop/edit_shop.html', form=form, shop=shop)
            
            db.session.commit()
            flash('Shop updated successfully!', 'success')
            return redirect(url_for('shop_dashboard'))
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error updating shop: {str(e)}")
            flash('An error occurred while updating the shop. Please try again.', 'error')
    
    # If form didn't validate or it's a GET request
    return render_template('shop/edit_shop.html', form=form, shop=shop)

@app.route('/shop/products', endpoint='shop_products')
@login_required
def shop_products():
    # Check if user is a shop owner and has shops
    if current_user.role != 'shopowner' or not hasattr(current_user, 'shops') or not current_user.shops.first():
        flash('You need to create a shop first to manage products!', 'warning')
        return redirect(url_for('create_shop'))
    
    try:
        # Get the first shop (assuming one shop per user for now)
        shop = current_user.shops.first()
        
        # Get search and category parameters
        search = request.args.get('search', '')
        category = request.args.get('category', '')
        
        # Build the base query
        query = Product.query.filter_by(shop_id=shop.id)
        
        # Apply filters if provided
        if search:
            query = query.filter(Product.name.ilike(f'%{search}%'))
        if category:
            query = query.filter_by(category=category)
        
        # Get unique categories for the filter dropdown
        categories = db.session.query(Product.category).filter_by(shop_id=shop.id).distinct().all()
        categories = [c[0] for c in categories if c[0]]
        
        # Get the filtered products
        products = query.order_by(Product.created_at.desc()).all()
        
        return render_template('shop/products.html', 
                             products=products, 
                             categories=categories,
                             search=search,
                             current_category=category,
                             shop=shop)
    except Exception as e:
        app.logger.error(f"Error in shop_products: {str(e)}")
        flash('An error occurred while loading products. Please try again.', 'error')
        return redirect(url_for('dashboard'))

@app.route('/shop/product/add', methods=['GET', 'POST'], endpoint='add_product')
@login_required
def add_product():
    if current_user.role != 'shopowner':
        flash('You need to be a shop owner to add products.', 'warning')
        return redirect(url_for('dashboard'))
    
    # Check for shop using the same method as in shop_dashboard
    shop = current_user.shops.first() if hasattr(current_user, 'shops') else None
    if not shop:
        flash('You need to create a shop first before adding products.', 'warning')
        return redirect(url_for('create_shop'))
    
    form = ProductForm()
    if form.validate_on_submit():
        image_path = None
        if form.image.data:
            image_path = save_image(form.image.data, 'products')
        
        product = Product(
            shop_id=shop.id,
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            category=form.category.data,
            image=image_path
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash('Product added successfully!', 'success')
        return redirect(url_for('shop_products'))
    
    return render_template('shop/add_product.html', form=form)

@app.route('/shop/product/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    if current_user.role != 'shopowner':
        return redirect(url_for('dashboard'))
    
    shop = current_user.shops.first()
    if not shop:
        flash('You need to create a shop first.', 'warning')
        return redirect(url_for('create_shop'))
    
    product = Product.query.get_or_404(product_id)
    
    # Verify the product belongs to the user's shop
    if product.shop_id != shop.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('shop_products'))
    
    form = ProductForm(obj=product)
    
    if form.validate_on_submit():
        try:
            product.name = form.name.data
            product.description = form.description.data
            product.price = form.price.data
            product.stock = form.stock.data
            product.category = form.category.data
            
            # Check if a new image was uploaded
            if hasattr(form.image.data, 'filename') and form.image.data.filename:
                # Delete old image if it exists
                if product.image:
                    try:
                        delete_image(product.image)
                    except Exception as e:
                        app.logger.error(f'Error deleting old image: {str(e)}')
                
                # Save new image
                try:
                    product.image = save_image(form.image.data, 'products')
                except Exception as e:
                    app.logger.error(f'Error saving new image: {str(e)}')
                    flash('Error updating product image. Please try again.', 'danger')
                    return render_template('shop/edit_product.html', form=form, product=product)
            
            db.session.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('shop_products'))
            
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'Error updating product: {str(e)}')
            flash('An error occurred while updating the product. Please try again.', 'danger')
    
    return render_template('shop/edit_product.html', form=form, product=product)

@app.route('/shop/product/<int:product_id>/delete', methods=['POST'])
@app.route('/shop/product/<int:product_id>/delete/', methods=['POST'])  # Handle with or without trailing slash
@login_required
def delete_product(product_id):
    if current_user.role != 'shopowner':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    shop = current_user.shops.first()
    if not shop:
        return jsonify({'success': False, 'message': 'Shop not found'}), 404
    
    product = Product.query.get_or_404(product_id)
    
    # Verify the product belongs to the user's shop
    if product.shop_id != shop.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        # Delete associated order items first (SQLite cascade delete workaround)
        OrderItem.query.filter_by(product_id=product_id).delete()
        
        # Delete the product image if it exists
        if product.image:
            try:
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], product.image)
                if os.path.exists(image_path):
                    os.remove(image_path)
            except Exception as e:
                app.logger.error(f'Error deleting product image: {str(e)}')
        
        db.session.delete(product)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Product deleted successfully', 'id': product_id})
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error deleting product: {str(e)}')
        return jsonify({'success': False, 'message': 'An error occurred while deleting the product'}), 500

@app.route('/shop/services', endpoint='shop_services')
@login_required
def shop_services():
    if current_user.role != 'shopowner':
        return redirect(url_for('dashboard'))
    
    shop = current_user.shops.first()
    if not shop:
        flash('You need to create a shop first.', 'warning')
        return redirect(url_for('create_shop'))
    
    services = Service.query.filter_by(shop_id=shop.id).all()
    return render_template('shop/services.html', services=services, shop=shop)

@app.route('/shop/service/add', methods=['GET', 'POST'], endpoint='add_service')
@login_required
def add_service():
    if current_user.role != 'shopowner':
        return redirect(url_for('dashboard'))
    
    shop = current_user.shops.first()
    if not shop:
        flash('You need to create a shop first.', 'warning')
        return redirect(url_for('create_shop'))
    
    form = ServiceForm()
    if form.validate_on_submit():
        image_path = None
        if form.image.data:
            image_path = save_image(form.image.data, 'services')
        
        service = Service(
            shop_id=shop.id,
            name=form.name.data,
            description=form.description.data,
            price=form.price.data,
            duration=form.duration.data,
            category=form.category.data,
            image=image_path
        )
        
        db.session.add(service)
        db.session.commit()
        
        flash('Service added successfully!', 'success')
        return redirect(url_for('shop_services'))
    
    return render_template('shop/add_service.html', form=form)

@app.route('/shop/service/edit/<int:service_id>', methods=['GET', 'POST'])
@login_required
def edit_service(service_id):
    if current_user.role != 'shopowner':
        return redirect(url_for('dashboard'))
    
    service = Service.query.get_or_404(service_id)
    
    if service.shop.owner_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('shop_services'))
    
    form = ServiceForm(obj=service)
    if form.validate_on_submit():
        service.name = form.name.data
        service.description = form.description.data
        service.price = form.price.data
        service.duration = form.duration.data
        service.category = form.category.data
        
        if form.image.data:
            if service.image:
                delete_image(service.image)
            service.image = save_image(form.image.data, 'services')
        
        db.session.commit()
        flash('Service updated successfully!', 'success')
        return redirect(url_for('shop_services'))
    
    return render_template('shop/edit_service.html', form=form, service=service)

@app.route('/shop/service/delete/<int:service_id>', methods=['POST'])
@login_required
def delete_service(service_id):
    if current_user.role != 'shopowner':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    service = Service.query.get_or_404(service_id)
    
    if service.shop.owner_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        # Delete associated service order items first (SQLite cascade delete workaround)
        ServiceOrderItem.query.filter_by(service_id=service_id).delete()
        
        if service.image:
            delete_image(service.image)
        
        db.session.delete(service)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Service deleted', 'id': service_id})
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error deleting service: {str(e)}')
        return jsonify({'success': False, 'message': 'An error occurred while deleting the service'}), 500

@app.route('/shop/orders', endpoint='shop_orders')
@login_required
def shop_orders():
    if current_user.role != 'shopowner':
        return redirect(url_for('dashboard'))
    
    shop = current_user.shops.first()
    if not shop:
        flash('You need to create a shop first.', 'warning')
        return redirect(url_for('create_shop'))
    
    order_items = OrderItem.query.filter_by(shop_id=shop.id).order_by(OrderItem.id.desc()).all()
    return render_template('shop/orders.html', order_items=order_items, shop=shop)

@app.route('/shop/order/update-status/<int:order_id>', methods=['POST'])
@login_required
def update_order_status(order_id):
    if current_user.role != 'shopowner':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    order = Order.query.get_or_404(order_id)
    status = request.json.get('status')
    
    if status not in ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']:
        return jsonify({'success': False, 'message': 'Invalid status'}), 400
    
    order.status = status
    db.session.commit()
    
    # Notify customer
    create_notification(
        order.customer_id,
        f'Your order #{order.order_number} status updated to: {status}'
    )
    
    return jsonify({'success': True, 'message': 'Order status updated'})

# ==================== ADMIN ROUTES ====================

@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    total_users = User.query.count()
    total_shops = Shop.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).filter_by(payment_status='completed').scalar() or 0
    
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html', 
                         total_users=total_users, total_shops=total_shops,
                         total_products=total_products, total_orders=total_orders,
                         total_revenue=total_revenue, recent_orders=recent_orders,
                         recent_users=recent_users)

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/user/toggle/<int:user_id>', methods=['POST'])
@login_required
def toggle_user(user_id):
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    user = User.query.get_or_404(user_id)
    
    if user.role == 'admin':
        return jsonify({'success': False, 'message': 'Cannot disable admin users'}), 400
    
    user.is_active = not user.is_active
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'User status updated', 'is_active': user.is_active})

@app.route('/admin/shops')
@login_required
def admin_shops():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    shops = Shop.query.order_by(Shop.created_at.desc()).all()
    return render_template('admin/shops.html', shops=shops)

@app.route('/admin/shop/toggle/<int:shop_id>', methods=['POST'])
@login_required
def toggle_shop(shop_id):
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    shop = Shop.query.get_or_404(shop_id)
    shop.is_active = not shop.is_active
    db.session.commit()
    
    # Notify shop owner
    create_notification(
        shop.owner_id,
        f'Your shop "{shop.name}" has been {"activated" if shop.is_active else "deactivated"} by admin.'
    )
    
    return jsonify({'success': True, 'message': 'Shop status updated', 'is_active': shop.is_active})

@app.route('/admin/products')
@login_required
def admin_products():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    products = Product.query.order_by(Product.created_at.desc()).all()
    return render_template('admin/products.html', products=products)

@app.route('/admin/product/toggle/<int:product_id>', methods=['POST'])
@login_required
def toggle_product(product_id):
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    product = Product.query.get_or_404(product_id)
    product.is_active = not product.is_active
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Product status updated', 'is_active': product.is_active})

@app.route('/admin/orders')
@login_required
def admin_orders():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('dashboard'))
    
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

# ==================== API ROUTES ====================

@app.route('/api/notifications')
@login_required
def get_notifications():
    notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False).order_by(Notification.created_at.desc()).limit(10).all()
    return jsonify({
        'notifications': [{
            'id': n.id,
            'message': n.message,
            'created_at': n.created_at.strftime('%Y-%m-%d %H:%M')
        } for n in notifications],
        'count': len(notifications)
    })

@app.route('/api/notification/read/<int:notification_id>', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    
    if notification.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    notification.is_read = True
    db.session.commit()
    
    return jsonify({'success': True})

@app.route('/api/cart/count')
@login_required
def cart_count():
    if current_user.role != 'customer':
        return jsonify({'count': 0})
    
    count = CartItem.query.filter_by(customer_id=current_user.id).count()
    return jsonify({'count': count})

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

# ==================== CONTEXT PROCESSORS ====================

@app.context_processor
def inject_csrf_token():
    from flask_wtf.csrf import generate_csrf
    # Return the function itself, not the result of calling it
    return {'csrf_token': generate_csrf}

@app.template_filter('format_currency')
def format_currency(value):
    if value is None:
        return "₹0"
    try:
        # Format with Indian numbering system (comma as thousand separator)
        return f"₹{float(value):,.2f}"
    except (ValueError, TypeError):
        return str(value)

@app.context_processor
def utility_processor():
    return dict(
        enumerate=enumerate,
        len=len,
        str=str
    )

# ==================== DATABASE INITIALIZATION ====================

def init_db():
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        admin = User.query.filter_by(email='admin@shopserv.com').first()
        if not admin:
            admin = User(
                email='admin@shopserv.com',
                full_name='Admin User',
                role='admin',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: admin@shopserv.com / admin123")

# ==================== MAIN ====================

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
