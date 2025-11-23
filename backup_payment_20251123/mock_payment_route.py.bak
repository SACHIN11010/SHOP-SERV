from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from ..models.models import db, Order, PaymentTransaction, CartItem, ServiceCartItem
from datetime import datetime, timedelta
import uuid
import logging

mock_payment = Blueprint('mock_payment', __name__)
logger = logging.getLogger(__name__)

def clear_user_cart():
    """Clear the user's cart after successful order"""
    try:
        CartItem.query.filter_by(customer_id=current_user.id).delete()
        ServiceCartItem.query.filter_by(customer_id=current_user.id).delete()
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error clearing cart for user {current_user.id}: {str(e)}")
        return False

def create_payment_transaction(order, payment_method):
    """Create a payment transaction record"""
    # Generate transaction IDs based on payment method
    if payment_method == 'upi':
        prefix = 'UPI'
        details = 'UPI Payment'
    elif payment_method == 'card':
        prefix = 'CARD'
        details = 'Credit/Debit Card Payment'
    else:
        prefix = 'PAY'
        details = 'Online Payment'
    
    transaction = PaymentTransaction(
        order_id=order.id,
        transaction_id=f"{prefix}{str(uuid.uuid4())[:13]}",
        payment_id=f"PAY{str(uuid.uuid4())[:13]}",
        amount=order.total_amount,
        currency='INR',
        status='completed',
        payment_method=payment_method,
        payment_details=details,
        metadata={
            'method': payment_method,
            'timestamp': datetime.utcnow().isoformat(),
            'user_agent': request.headers.get('User-Agent')
        }
    )
    
    return transaction

@mock_payment.route('/process-payment/<int:order_id>')
@login_required
def process_payment(order_id):
    """Process payment based on the selected method"""
    payment_method = request.args.get('method', 'card')
    
    # Get the order with related data
    order = Order.query.options(
        db.joinedload(Order.customer)
    ).filter_by(
        id=order_id, 
        customer_id=current_user.id
    ).first_or_404()
    
    # Validate order status
    if order.payment_status != 'pending':
        flash('This order has already been processed', 'warning')
        return redirect(url_for('customer.orders'))
    
    # Handle UPI payment (show QR page)
    if payment_method == 'upi':
        # Get shop's UPI ID if available, otherwise use default
        shop_upi_id = None
        if order.items.first() and order.items.first().shop:
            shop_upi_id = order.items.first().shop.upi_id
        
        upi_id = shop_upi_id or 'shopandserv@upi'
        
        return render_template(
            'customer/qr_payment.html',
            order=order,
            upi_id=upi_id,
            amount=order.total_amount,
            timestamp=int(datetime.utcnow().timestamp())
        )
    
    # For card payments, process directly
    elif payment_method == 'card':
        return redirect(url_for('mock_payment.confirm_payment', order_id=order.id, method=payment_method))
    
    # Invalid payment method
    flash('Invalid payment method selected', 'danger')
    return redirect(url_for('customer.checkout'))

@mock_payment.route('/confirm-payment/<int:order_id>')
@login_required
def confirm_payment(order_id):
    """Confirm a payment (for card payments)"""
    payment_method = request.args.get('method', 'card')
    
    # Start a transaction
    with db.session.begin_nested():
        # Get the order with row-level locking to prevent race conditions
        order = Order.query.with_for_update().filter_by(
            id=order_id, 
            customer_id=current_user.id
        ).first_or_404()
        
        # Validate order status
        if order.payment_status != 'pending':
            flash('This order has already been processed', 'warning')
            return redirect(url_for('customer.orders'))
        
        try:
            # Create and save payment transaction
            transaction = create_payment_transaction(order, payment_method)
            db.session.add(transaction)
            
            # Update order status
            order.payment_status = 'paid'
            order.status = 'confirmed'
            order.payment_intent_id = transaction.transaction_id
            order.paid_at = datetime.utcnow()
            
            # Clear the cart
            cart_cleared = clear_user_cart()
            if not cart_cleared:
                logger.warning(f"Failed to clear cart for order {order.id}")
            
            db.session.commit()
            
            # Redirect to success page
            return redirect(url_for('customer.order_success', order_id=order.id))
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error processing payment for order {order_id}: {str(e)}", exc_info=True)
            flash('An error occurred while processing your payment. Please try again.', 'danger')
            return redirect(url_for('customer.checkout'))

@mock_payment.route('/qr-payment/verify', methods=['POST'])
@login_required
def verify_qr_payment():
    """Verify UPI payment (called via AJAX from the QR payment page)"""
    order_id = request.form.get('order_id')
    upi_id = request.form.get('upi_id', '')
    
    if not order_id:
        return jsonify({
            'success': False,
            'message': 'Missing order ID'
        }), 400
    
    # Start a transaction
    with db.session.begin_nested():
        try:
            # Get the order with row-level locking
            order = Order.query.with_for_update().filter_by(
                id=order_id,
                customer_id=current_user.id,
                payment_status='pending'
            ).first()
            
            if not order:
                return jsonify({
                    'success': False,
                    'message': 'Order not found or already processed',
                    'redirect': url_for('customer.orders')
                }), 404
            
            # Create and save payment transaction
            transaction = create_payment_transaction(order, 'upi')
            transaction.payment_details = f"UPI Payment to {upi_id}"
            db.session.add(transaction)
            
            # Update order status
            order.payment_status = 'paid'
            order.status = 'confirmed'
            order.payment_intent_id = transaction.transaction_id
            order.paid_at = datetime.utcnow()
            
            # Clear the cart
            cart_cleared = clear_user_cart()
            if not cart_cleared:
                logger.warning(f"Failed to clear cart for order {order.id}")
            
            db.session.commit()
            
            # Return success response
            return jsonify({
                'success': True,
                'message': 'Payment successful',
                'redirect': url_for('customer.order_success', order_id=order.id)
            })
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error verifying UPI payment for order {order_id}: {str(e)}", exc_info=True)
            return jsonify({
                'success': False,
                'message': 'An error occurred while processing your payment. Please try again.'
            }), 500

@mock_payment.route('/payment/cancel')
@login_required
def payment_cancel():
    """Handle payment cancellation"""
    order_id = request.args.get('order_id')
    
    if order_id:
        # Optional: Update order status to reflect cancellation
        try:
            order = Order.query.filter_by(
                id=order_id,
                customer_id=current_user.id,
                payment_status='pending'
            ).first()
            
            if order:
                order.status = 'cancelled'
                order.payment_status = 'cancelled'
                db.session.commit()
                
                flash('Your payment was cancelled and the order has been cancelled.', 'info')
                return redirect(url_for('customer.orders'))
                
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error cancelling order {order_id}: {str(e)}")
    
    flash('Payment was cancelled', 'info')
    return redirect(url_for('customer.cart'))
