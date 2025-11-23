from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, RadioField, SubmitField, validators
from wtforms.validators import DataRequired, Length, Regexp

class CheckoutForm(FlaskForm):
    """Form for handling checkout process"""
    
    # Payment method choices
    PAYMENT_METHODS = [
        ('cod', 'Cash on Delivery (COD)'),
        ('card', 'Credit/Debit Card'),
        ('upi', 'UPI / QR Code')
    ]
    
    # Form fields
    payment_method = RadioField(
        'Payment Method',
        choices=PAYMENT_METHODS,
        validators=[DataRequired(message='Please select a payment method')],
        default='cod'
    )
    
    shipping_address = StringField(
        'Delivery Address',
        validators=[
            DataRequired(message='Please enter a shipping address'),
            Length(min=10, max=200, message='Address must be between 10 and 200 characters')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Enter your full shipping address'
        }
    )
    
    shipping_phone = StringField(
        'Phone Number',
        validators=[
            DataRequired(message='Please enter a phone number'),
            Regexp('^[0-9]{10}$', message='Please enter a valid 10-digit phone number')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Enter your 10-digit phone number'
        }
    )
    
    notes = TextAreaField(
        'Order Notes (Optional)',
        validators=[
            Length(max=500, message='Notes cannot exceed 500 characters')
        ],
        render_kw={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Any special instructions for your order...'
        }
    )
    
    submit = SubmitField(
        'Place Order',
        render_kw={
            'class': 'btn btn-primary btn-lg btn-block',
            'id': 'place-order-btn'
        }
    )
