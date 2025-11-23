from flask import Blueprint, jsonify, request, redirect, url_for, flash, current_app, session
from flask_login import login_required, current_user
from ..models.models import db, CartItem, Product, ServiceCartItem, Service, Order, OrderItem, ServiceOrderItem
from functools import wraps
from datetime import datetime
import uuid

cart_bp = Blueprint('cart', __name__)

def get_cart_items():
    """Helper function to get cart items for the current user"""
    cart_items = CartItem.query.filter_by(customer_id=current_user.id).all()
    service_cart_items = ServiceCartItem.query.filter_by(customer_id=current_user.id).all()
    return cart_items, service_cart_items

def calculate_cart_totals():
    """Calculate cart totals and return cart data"""
    try:
        cart_items, service_cart_items = get_cart_items()
        
        total = 0
        cart_products = []
        cart_services = []
        
        for item in cart_items:
            if item.product and item.product.is_active:
                item_total = item.product.price * item.quantity
                total += item_total
                cart_products.append({
                    'id': item.id,
                    'product_id': item.product.id,
                    'name': item.product.name,
                    'price': item.product.price,
                    'quantity': item.quantity,
                    'image': item.product.image or 'images/placeholder-product.jpg',
                    'subtotal': item_total
                })
        
        for item in service_cart_items:
            if item.service and item.service.is_active:
                item_total = item.service.price * item.quantity
                total += item_total
                cart_services.append({
                    'id': item.id,
                    'service_id': item.service.id,
                    'name': item.service.name,
                    'price': item.service.price,
                    'quantity': item.quantity,
                    'image': item.service.image or 'images/placeholder-service.jpg',
                    'subtotal': item_total
                })
        
        return {
            'success': True,
            'total': total,
            'item_count': len(cart_products) + len(cart_services),
            'products': cart_products,
            'services': cart_services
        }
    except Exception as e:
        current_app.logger.error(f'Error calculating cart totals: {str(e)}')
        return {
            'success': False,
            'total': 0,
            'item_count': 0,
            'products': [],
            'services': []
        }

@cart_bp.route('/api/cart', methods=['GET'])
@login_required
def get_cart():
    """Get cart contents as JSON"""
    return jsonify({
        'success': True,
        'cart': calculate_cart_totals()
    })

@cart_bp.route('/api/cart/add/product/<int:product_id>', methods=['POST'])
@login_required
def add_product_to_cart(product_id):
    """Add a product to cart"""
    try:
        quantity = int(request.json.get('quantity', 1)) if request.is_json else int(request.form.get('quantity', 1))
        
        # Check if product exists and is active
        product = Product.query.filter_by(id=product_id, is_active=True).first()
        if not product:
            return jsonify({'success': False, 'message': 'Product not found or unavailable'}), 404
        
        # Check if product is already in cart
        cart_item = CartItem.query.filter_by(
            customer_id=current_user.id, 
            product_id=product_id
        ).first()
        
        if cart_item:
            # Update quantity if already in cart
            cart_item.quantity += quantity
        else:
            # Add new item to cart
            cart_item = CartItem(
                customer_id=current_user.id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(cart_item)
        
        db.session.commit()
        cart_data = calculate_cart_totals()
        return jsonify({
            'success': True,
            'message': 'Product added to cart',
            'cart_count': cart_data['item_count'],
            'cart': cart_data
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error adding product to cart: {str(e)}')
        return jsonify({'success': False, 'message': 'Failed to add product to cart'}), 500

@cart_bp.route('/api/cart/update/<int:item_id>', methods=['POST'])
@login_required
def update_cart_item(item_id):
    """Update cart item quantity"""
    try:
        data = request.get_json()
        quantity = int(data.get('quantity', 1))
        
        cart_item = CartItem.query.filter_by(id=item_id, customer_id=current_user.id).first()
        if not cart_item:
            return jsonify({'success': False, 'message': 'Item not found in cart'}), 404
        
        if quantity <= 0:
            db.session.delete(cart_item)
        else:
            cart_item.quantity = quantity
        
        db.session.commit()
        
        cart_data = calculate_cart_totals()
        return jsonify({
            'success': True,
            'message': 'Cart updated',
            'cart': cart_data
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error updating cart item: {str(e)}')
        return jsonify({'success': False, 'message': 'Failed to update cart'}), 500

@cart_bp.route('/api/cart/remove/product/<int:item_id>', methods=['POST', 'DELETE'])
@login_required
def remove_product_from_cart(item_id):
    """Remove a product from cart"""
    try:
        cart_item = CartItem.query.filter_by(
            id=item_id,
            customer_id=current_user.id
        ).first()
        
        if not cart_item:
            return jsonify({'success': False, 'message': 'Item not found in cart'}), 404
        
        db.session.delete(cart_item)
        db.session.commit()
        
        cart_data = calculate_cart_totals()
        return jsonify({
            'success': True,
            'message': 'Product removed from cart',
            'cart_count': cart_data['item_count'],
            'cart': cart_data
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error removing product from cart: {str(e)}')
        return jsonify({'success': False, 'message': 'Failed to remove product from cart'}), 500

# Service cart routes (similar to product routes)
@cart_bp.route('/api/cart/add/service/<int:service_id>', methods=['POST'])
@login_required
def add_service_to_cart(service_id):
    """Add a service to cart"""
    try:
        quantity = int(request.json.get('quantity', 1)) if request.is_json else int(request.form.get('quantity', 1))
        
        service = Service.query.filter_by(id=service_id, is_active=True).first()
        if not service:
            return jsonify({'success': False, 'message': 'Service not found or unavailable'}), 404
        
        cart_item = ServiceCartItem.query.filter_by(
            customer_id=current_user.id, 
            service_id=service_id
        ).first()
        
        if cart_item:
            cart_item.quantity += quantity
        else:
            cart_item = ServiceCartItem(
                customer_id=current_user.id,
                service_id=service_id,
                quantity=quantity
            )
            db.session.add(cart_item)
        
        db.session.commit()
        cart_data = calculate_cart_totals()
        return jsonify({
            'success': True,
            'message': 'Service added to cart',
            'cart_count': cart_data['item_count'],
            'cart': cart_data
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error adding service to cart: {str(e)}')
        return jsonify({'success': False, 'message': 'Failed to add service to cart'}), 500

@cart_bp.route('/api/cart/update/service/<int:item_id>', methods=['POST'])
@login_required
def update_service_cart_item(item_id):
    """Update service cart item quantity"""
    try:
        data = request.get_json() if request.is_json else request.form.to_dict()
        if not data or 'quantity' not in data:
            return jsonify({'success': False, 'message': 'Invalid request'}), 400
        
        quantity = int(data['quantity'])
        if quantity < 1:
            return jsonify({'success': False, 'message': 'Quantity must be at least 1'}), 400
        
        cart_item = ServiceCartItem.query.filter_by(id=item_id, customer_id=current_user.id).first()
        if not cart_item:
            return jsonify({'success': False, 'message': 'Item not found in cart'}), 404
        
        cart_item.quantity = quantity
        db.session.commit()
        
        cart_data = calculate_cart_totals()
        return jsonify({
            'success': True,
            'message': 'Cart updated',
            'cart': cart_data
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error updating cart: {str(e)}')
        return jsonify({'success': False, 'message': 'Failed to update cart'}), 500

@cart_bp.route('/api/cart/remove/service/<int:item_id>', methods=['POST', 'DELETE'])
@login_required
def remove_service_from_cart(item_id):
    """Remove a service from cart"""
    try:
        cart_item = ServiceCartItem.query.filter_by(
            id=item_id,
            customer_id=current_user.id
        ).first()
        
        if not cart_item:
            return jsonify({'success': False, 'message': 'Item not found in cart'}), 404
        
        db.session.delete(cart_item)
        db.session.commit()
        
        cart_data = calculate_cart_totals()
        return jsonify({
            'success': True,
            'message': 'Service removed from cart',
            'cart_count': cart_data['item_count'],
            'cart': cart_data
        })
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error removing service from cart: {str(e)}')
        return jsonify({'success': False, 'message': 'Failed to remove service from cart'}), 500
