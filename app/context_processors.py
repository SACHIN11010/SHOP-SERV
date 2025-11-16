"""
Context processors for the SHOP_SERV application.
These make variables available to all templates.
"""
from datetime import datetime
from flask import current_app, session, g

def inject_now():
    """Inject the current datetime into all templates as 'now'."""
    return {'now': datetime.utcnow()}

def inject_config():
    """Inject selected configuration variables into all templates."""
    return {
        'app_name': current_app.config.get('APP_NAME', 'SHOP_SERV'),
        'debug': current_app.config.get('DEBUG', False),
    }

def inject_user():
    """Inject user-related variables into all templates."""
    from flask_login import current_user
    
    user_data = {
        'current_user': current_user,
        'is_authenticated': current_user.is_authenticated,
    }
    
    if current_user.is_authenticated:
        user_data.update({
            'is_admin': current_user.role == 'admin',
            'is_shop_owner': current_user.role == 'shop_owner',
            'is_customer': current_user.role == 'customer',
            'cart_count': current_user.cart_items.count() + current_user.service_cart_items.count()
        })
    
    return user_data

def inject_global_vars():
    """Inject global variables into all templates."""
    return {
        'year': datetime.utcnow().year,
        'stripe_public_key': current_app.config.get('STRIPE_PUBLIC_KEY', ''),
        'upn_id': current_app.config.get('UPI_ID', ''),
    }

def init_app(app):
    """Register context processors with the Flask application."""
    app.context_processor(inject_now)
    app.context_processor(inject_config)
    app.context_processor(inject_user)
    app.context_processor(inject_global_vars)
