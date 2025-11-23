from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from datetime import datetime
import uuid
import os
from ..models.models import db, Order, OrderItem, ServiceOrderItem, CartItem, ServiceCartItem

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

def generate_order_number():
    """Generate a unique order number"""
    return f"ORD-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}"

@payment_bp.route('/<int:order_id>', methods=['GET'])
@login_required
def payment_options(order_id):
    """Show payment options for an order"""
    order = Order.query.filter_by(id=order_id, customer_id=current_user.id).first_or_404()
    
    if order.status != 'pending':
        flash('This order has already been processed', 'warning')
        return redirect(url_for('customer.orders'))
    
    return render_template('payment/options.html', order=order)

@payment_bp.route('/process', methods=['POST'])
@login_required
def process_payment():
    """Process payment for an order"""
    order_id = request.form.get('order_id')
    payment_method = request.form.get('payment_method')
    
    if not order_id or not payment_method:
        flash('Invalid request', 'error')
        return redirect(url_for('customer.orders'))
    
    order = Order.query.filter_by(id=order_id, customer_id=current_user.id).first()
    if not order:
        flash('Order not found', 'error')
        return redirect(url_for('customer.orders'))
    
    if order.status != 'pending':
        flash('This order has already been processed', 'warning')
        return redirect(url_for('customer.orders'))
    
    # Process payment based on method
    try:
        if payment_method == 'cod':
            # For COD, just mark as paid
            order.payment_status = 'pending'
            order.status = 'confirmed'
            order.payment_method = 'cod'
            db.session.commit()
            
            # Clear the cart
            CartItem.query.filter_by(customer_id=current_user.id).delete()
            ServiceCartItem.query.filter_by(customer_id=current_user.id).delete()
            db.session.commit()
            
            return redirect(url_for('payment.success', order_id=order.id))
            
        elif payment_method in ['card', 'upi']:
            # For card/UPI, redirect to demo payment page
            return redirect(url_for(f'payment.{payment_method}_payment', order_id=order.id))
            
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error processing payment: {str(e)}')
        flash('An error occurred while processing your payment. Please try again.', 'error')
    
    return redirect(url_for('payment.payment_options', order_id=order.id))

@payment_bp.route('/card/<int:order_id>', methods=['GET'])
@login_required
def card_payment(order_id):
    """Show card payment form (demo)"""
    order = Order.query.filter_by(id=order_id, customer_id=current_user.id).first_or_404()
    
    if order.status != 'pending':
        flash('This order has already been processed', 'warning')
        return redirect(url_for('customer.orders'))
    
    return render_template('payment/card.html', order=order)

@payment_bp.route('/card/confirm/<int:order_id>', methods=['POST'])
@login_required
def confirm_card_payment(order_id):
    """Confirm card payment (demo)"""
    order = Order.query.filter_by(id=order_id, customer_id=current_user.id).first_or_404()
    
    if order.status != 'pending':
        flash('This order has already been processed', 'warning')
        return redirect(url_for('customer.orders'))
    
    try:
        # Mark as paid
        order.payment_status = 'paid'
        order.status = 'confirmed'
        order.payment_method = 'card'
        order.payment_date = datetime.utcnow()
        
        # Generate a fake transaction ID
        order.transaction_id = f"TXN{str(uuid.uuid4())[:13].upper()}"
        
        # Clear the cart
        CartItem.query.filter_by(customer_id=current_user.id).delete()
        ServiceCartItem.query.filter_by(customer_id=current_user.id).delete()
        
        db.session.commit()
        
        # In a real app, you would process the payment here
        # For demo, we'll just redirect to success
        return redirect(url_for('payment.success', order_id=order.id))
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error confirming card payment: {str(e)}')
        flash('An error occurred while processing your payment. Please try again.', 'error')
        return redirect(url_for('payment.card_payment', order_id=order.id))

@payment_bp.route('/upi/<int:order_id>', methods=['GET'])
@login_required
def upi_payment(order_id):
    """Show UPI payment page (demo)"""
    order = Order.query.filter_by(id=order_id, customer_id=current_user.id).first_or_404()
    
    if order.status != 'pending':
        flash('This order has already been processed', 'warning')
        return redirect(url_for('customer.orders'))
    
    # Generate a UPI ID if not exists
    if not order.upi_id:
        order.upi_id = f"shopandserv-{order.id}@upi"
        db.session.commit()
    
    return render_template('payment/upi.html', order=order)

@payment_bp.route('/upi/confirm/<int:order_id>', methods=['POST'])
@login_required
def confirm_upi_payment(order_id):
    """Confirm UPI payment (demo)"""
    order = Order.query.filter_by(id=order_id, customer_id=current_user.id).first_or_404()
    
    if order.status != 'pending':
        flash('This order has already been processed', 'warning')
        return redirect(url_for('customer.orders'))
    
    try:
        # Mark as paid
        order.payment_status = 'paid'
        order.status = 'confirmed'
        order.payment_method = 'upi'
        order.payment_date = datetime.utcnow()
        
        # Generate a fake UPI transaction ID
        order.transaction_id = f"UPI{str(uuid.uuid4())[:13].upper()}"
        
        # Clear the cart
        CartItem.query.filter_by(customer_id=current_user.id).delete()
        ServiceCartItem.query.filter_by(customer_id=current_user.id).delete()
        
        db.session.commit()
        
        return redirect(url_for('payment.success', order_id=order.id))
        
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error confirming UPI payment: {str(e)}')
        flash('An error occurred while processing your payment. Please try again.', 'error')
        return redirect(url_for('payment.upi_payment', order_id=order.id))

@payment_bp.route('/success/<int:order_id>', methods=['GET'])
@login_required
def success(order_id):
    """Show order success page"""
    order = Order.query.filter_by(id=order_id, customer_id=current_user.id).first_or_404()
    
    if order.status == 'pending':
        # This shouldn't happen, but just in case
        flash('Your order is still being processed. Please check back later.', 'info')
        return redirect(url_for('customer.orders'))
    
    return render_template('payment/success.html', order=order)
