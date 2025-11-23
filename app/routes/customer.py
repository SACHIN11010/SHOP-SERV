from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from ..models.models import db, CartItem, Product, ServiceCartItem, Service, Order, OrderItem, ServiceOrderItem, PaymentTransaction, Shop
from datetime import datetime, timedelta
import uuid
import logging

customer = Blueprint('customer', __name__)
logger = logging.getLogger(__name__)

def get_cart_data():
    """Get cart items and calculate totals"""
    cart_items = CartItem.query.filter_by(customer_id=current_user.id).all()
    service_cart_items = ServiceCartItem.query.filter_by(customer_id=current_user.id).all()
    
    total = 0
    cart_products = []
    cart_services = []
    shop_ids = set()
    
    # Process product cart items
    for item in cart_items:
        if item.product and item.product.is_active:
            product_total = item.product.price * item.quantity
            total += product_total
            cart_products.append(item)
            shop_ids.add(item.product.shop_id)
    
    # Process service cart items
    for item in service_cart_items:
        if item.service and item.service.is_active:
            service_total = item.service.price * item.quantity
            total += service_total
            cart_services.append(item)
            shop_ids.add(item.service.shop_id)
    
    # Get shop details
    shops = Shop.query.filter(Shop.id.in_(shop_ids)).all() if shop_ids else []
    
    return {
        'total': total,
        'products': cart_products,
        'services': cart_services,
        'shops': {shop.id: shop for shop in shops},
        'item_count': len(cart_products) + len(cart_services)
    }

@customer.route('/cart')
@login_required
def cart():
    """View cart page"""
    cart_data = get_cart_data()
    return render_template('customer/cart.html', **cart_data)

@customer.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout process"""
    from ..forms import CheckoutForm
    from flask_wtf.csrf import generate_csrf
    
    cart_data = get_cart_data()
    
    if not cart_data['products'] and not cart_data['services']:
        flash('Your cart is empty!', 'warning')
        return redirect(url_for('customer.cart'))
    
    form = CheckoutForm()
    if form.validate_on_submit():
        try:
            payment_method = form.payment_method.data
            shipping_address = form.shipping_address.data
            shipping_phone = form.shipping_phone.data
            notes = form.notes.data
            
            # Create order
            order = Order(
                order_number=f"ORD-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8]}",
                customer_id=current_user.id,
                total_amount=cart_data['total'],
                status='pending',
                payment_status='pending',
                payment_method=payment_method,
                shipping_address=shipping_address,
                shipping_phone=shipping_phone,
                notes=notes
            )
            
            db.session.add(order)
            db.session.flush()  # Get the order ID
            
            # Add order items
            for item in cart_data['products']:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item.product.id,
                    shop_id=item.product.shop_id,
                    quantity=item.quantity,
                    price=item.product.price,
                    name=item.product.name,
                    image=item.product.image
                )
                db.session.add(order_item)
            
            for item in cart_data['services']:
                service_item = ServiceOrderItem(
                    order_id=order.id,
                    service_id=item.service.id,
                    shop_id=item.service.shop_id,
                    quantity=item.quantity,
                    price=item.service.price,
                    name=item.service.name,
                    image=item.service.image
                )
                db.session.add(service_item)
            
            # Handle payment based on method
            if payment_method == 'cod':
                order.payment_status = 'pending'
                order.status = 'confirmed'
                db.session.commit()
                
                # Clear cart
                CartItem.query.filter_by(customer_id=current_user.id).delete()
                ServiceCartItem.query.filter_by(customer_id=current_user.id).delete()
                db.session.commit()
                
                return redirect(url_for('customer.order_success', order_id=order.id))
                
            elif payment_method in ['card', 'upi']:
                db.session.commit()
                # Redirect to payment processing
                return redirect(url_for('mock_payment.process_payment', order_id=order.id, method=payment_method))
            
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Checkout error: {str(e)}", exc_info=True)
            flash('An error occurred while processing your order. Please try again.', 'danger')
    
    # For GET request or form validation failed
    # Prepare cart items for display
    products = []
    services = []
    
    for item in cart_data['products']:
        products.append({
            'id': item.id,
            'name': item.product.name,
            'price': item.product.price,
            'quantity': item.quantity,
            'image': item.product.image or 'images/placeholder-product.jpg',
            'subtotal': item.product.price * item.quantity
        })
    
    for item in cart_data['services']:
        services.append({
            'id': item.id,
            'name': item.service.name,
            'price': item.service.price,
            'quantity': item.quantity,
            'image': item.service.image or 'images/placeholder-service.jpg',
            'subtotal': item.service.price * item.quantity
        })
    
    # Pre-fill form with user data if available
    if not form.shipping_address.data and current_user.address:
        form.shipping_address.data = current_user.address
    if not form.shipping_phone.data and current_user.phone:
        form.shipping_phone.data = current_user.phone
    
    # Generate CSRF token
    csrf_token = generate_csrf()
    
    return render_template('customer/checkout.html',
                         form=form,
                         products=products,
                         services=services,
                         total=cart_data['total'],
                         cart_item_count=cart_data['item_count'],
                         csrf_token=csrf_token)
        
        try:
            # Start transaction
            with db.session.begin_nested():
                # Create order
                order = Order(
                    order_number=f"ORD-{datetime.utcnow().strftime('%Y%m%d')}-{current_user.id}-{str(uuid.uuid4())[:8]}",
                    customer_id=current_user.id,
                    total_amount=cart_data['total'],
                    status='pending',
                    payment_status='pending',
                    payment_method=payment_method,
                    shipping_address=shipping_address,
                    shipping_phone=shipping_phone,
                    notes=request.form.get('notes', '')
                )
                db.session.add(order)
                db.session.flush()  # Get the order ID
                
                # Add product order items
                for item in cart_data['products']:
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=item.product_id,
                        shop_id=item.product.shop_id,
                        quantity=item.quantity,
                        price=item.product.price,
                        name=item.product.name,
                        image=item.product.image
                    )
                    db.session.add(order_item)
                
                # Add service order items
                for item in cart_data['services']:
                    service_item = ServiceOrderItem(
                        order_id=order.id,
                        service_id=item.service_id,
                        shop_id=item.service.shop_id,
                        quantity=item.quantity,
                        price=item.service.price,
                        name=item.service.name,
                        image=item.service.image
                    )
                    db.session.add(service_item)
                
                # Handle payment based on method
                if payment_method == 'cod':
                    order.payment_status = 'pending'
                    order.status = 'confirmed'
                    
                    # Create a payment transaction for COD
                    transaction = PaymentTransaction(
                        order_id=order.id,
                        transaction_id=f"COD-{str(uuid.uuid4())[:13]}",
                        amount=order.total_amount,
                        currency='INR',
                        status='pending',
                        payment_method='cod',
                        payment_details='Cash on Delivery'
                    )
                    db.session.add(transaction)
                    
                    # Clear cart after successful order
                    CartItem.query.filter_by(customer_id=current_user.id).delete()
                    ServiceCartItem.query.filter_by(customer_id=current_user.id).delete()
                    
                    db.session.commit()
                    
                    return redirect(url_for('customer.order_success', order_id=order.id))
                
                else:
                    # For online payments, mark as pending and redirect to payment
                    order.payment_status = 'pending'
                    db.session.commit()
                    
                    return redirect(url_for('mock_payment.process_payment', 
                                         order_id=order.id, 
                                         method=payment_method))
        
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error during checkout: {str(e)}", exc_info=True)
            flash('An error occurred while processing your order. Please try again.', 'danger')
            return redirect(url_for('customer.checkout'))
    
    # GET request - show checkout form
    return render_template('customer/checkout.html', 
                         total=cart_data['total'],
                         cart_items=cart_data['products'] + cart_data['services'],
                         shops=cart_data['shops'])
    
    return render_template('customer/checkout.html', total=total)

@customer.route('/order/success/<int:order_id>')
@login_required
def order_success(order_id):
    """Order success page"""
    order = Order.query.options(
        db.joinedload(Order.items).joinedload(OrderItem.product),
        db.joinedload(Order.service_items).joinedload(ServiceOrderItem.service)
    ).get_or_404(order_id)
    
    if order.customer_id != current_user.id and not current_user.is_admin:
        flash('You are not authorized to view this order', 'danger')
        return redirect(url_for('main.home'))
    
    # Calculate delivery estimate (2-5 days from now)
    delivery_date = datetime.utcnow() + timedelta(days=3)
    
    return render_template('customer/order_success.html', 
                         order=order,
                         delivery_date=delivery_date.strftime('%A, %B %d, %Y'))

@customer.route('/order/cancel/<int:order_id>', methods=['POST'])
@login_required
def cancel_order(order_id):
    """Cancel an order"""
    order = Order.query.get_or_404(order_id)
    
    # Check authorization
    if order.customer_id != current_user.id and not current_user.is_admin:
        return jsonify({
            'success': False, 
            'message': 'You are not authorized to cancel this order'
        }), 403
    
    # Check if order can be cancelled
    if order.status not in ['pending', 'confirmed']:
        return jsonify({
            'success': False, 
            'message': f'Cannot cancel order in {order.status} status'
        }), 400
    
    try:
        # Update order status
        order.status = 'cancelled'
        
        # Update payment status if paid
        if order.payment_status == 'paid':
            order.payment_status = 'refund_pending'
            
            # Create refund transaction
            refund = PaymentTransaction(
                order_id=order.id,
                transaction_id=f"RFND-{str(uuid.uuid4())[:13]}",
                amount=order.total_amount,
                currency='INR',
                status='pending',
                payment_method=order.payment_method,
                payment_details=f'Refund for order #{order.order_number}'
            )
            db.session.add(refund)
        
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Order cancelled successfully',
            'redirect': url_for('customer.orders')
        })
    
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error cancelling order {order_id}: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'message': 'An error occurred while cancelling the order'
        }), 500
