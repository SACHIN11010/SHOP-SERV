from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, time
from sqlalchemy.ext.hybrid import hybrid_property

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), nullable=False, default='customer')  # customer, shopowner, admin
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    shop = db.relationship('Shop', backref='owner', uselist=False, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='customer', lazy='dynamic', foreign_keys='Order.customer_id')
    cart_items = db.relationship('CartItem', backref='customer', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.email}>'

class Shop(db.Model):
    __tablename__ = 'shops'
    
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    logo = db.Column(db.String(200))
    address = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(20))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    delivery_radius_km = db.Column(db.Float, default=5.0)
    delivery_charge = db.Column(db.Float, default=0.0)
    min_order_amount = db.Column(db.Float, default=0.0)
    opening_time = db.Column(db.Time, default=time(9, 0))  # 9:00 AM
    closing_time = db.Column(db.Time, default=time(21, 0))  # 9:00 PM
    is_verified = db.Column(db.Boolean, default=False)
    service_type = db.Column(db.String(50))
    contact_phone = db.Column(db.String(20))
    contact_whatsapp = db.Column(db.String(20))
    contact_email = db.Column(db.String(120))
    is_delivery_available = db.Column(db.Boolean, default=True)
    is_pickup_available = db.Column(db.Boolean, default=True)
    is_cod_available = db.Column(db.Boolean, default=True)
    average_rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    is_approved = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='shop', lazy='dynamic', cascade='all, delete-orphan')
    services = db.relationship('Service', backref='shop', lazy='dynamic', cascade='all, delete-orphan')
    shop_reviews = db.relationship('Review', backref='shop', lazy='dynamic')
    
    @hybrid_property
    def is_open(self):
        if not self.opening_time or not self.closing_time:
            return True
        now = datetime.now().time()
        return self.opening_time <= now <= self.closing_time
    
    def update_average_rating(self):
        if self.shop_reviews.count() > 0:
            self.average_rating = self.shop_reviews.with_entities(
                db.func.avg(Review.rating)
            ).scalar() or 0.0
            self.review_count = self.shop_reviews.count()
            db.session.commit()
    
    def __repr__(self):
        return f'<Shop {self.name}>'

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    product = db.relationship('Product', backref='reviews')
    order = db.relationship('Order', backref='review')
    
    def __repr__(self):
        return f'<Review {self.rating} by User {self.user_id}>'
