from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def create_app(config_class='config.Config'):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize CSRF protection
    csrf.init_app(app)
    
    # Initialize rate limiter
    limiter.init_app(app)
    
    # Make CSRF token available in all templates
    @app.context_processor
    def inject_csrf_token():
        from flask_wtf.csrf import generate_csrf
        return {'csrf_token': generate_csrf}
        
    # Import and register blueprints
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    from .shop import shop as shop_blueprint
    
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(shop_blueprint, url_prefix='/shop')

    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    # Register blueprints - these are imported in app.py and shops_route.py
    # Blueprints will be registered in those files directly

    # Create upload folders
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'products'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'shops'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'services'), exist_ok=True)

    # Error handlers
    from .errors import page_not_found, forbidden, internal_server_error
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(500, internal_server_error)

    # Context processors
    from .context_processors import inject_now
    app.context_processor(inject_now)

    # Shell context
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Shop': Shop,
            'Product': Product,
            'Service': Service,
            'Order': Order,
            'OTP': OTP,
            'CartItem': CartItem,
            'ServiceCartItem': ServiceCartItem,
            'OrderItem': OrderItem,
            'ServiceOrderItem': ServiceOrderItem,
            'Notification': Notification
        }

    return app

# Import models here to avoid circular imports
from .models.models import db, User, Shop, Product, Service, Order, OTP, CartItem, ServiceCartItem, OrderItem, ServiceOrderItem, Notification  # noqa
