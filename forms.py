from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, TextAreaField, FloatField, IntegerField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange, Optional, Regexp
from app.models.models import User

class RegistrationForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Register As', choices=[('customer', 'Customer'), ('shopowner', 'Shop Owner')], validators=[DataRequired()])
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower()).first()
        if user:
            raise ValidationError('Email already registered. Please use a different email.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

class VerifyOTPForm(FlaskForm):
    otp = StringField('OTP Code', validators=[DataRequired(), Length(min=6, max=6)])

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

class ProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])

class ShopForm(FlaskForm):
    # Basic Information
    name = StringField('Shop Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    service_type = StringField('Business Type (e.g., Bakery, Electronics, Grocery)', 
                             validators=[DataRequired(), Length(max=50)])
    logo = FileField('Shop Logo', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Only image files are allowed')
    ])
    
    # Location Information
    address = StringField('Full Address', validators=[DataRequired(), Length(max=200)])
    city = StringField('City', validators=[DataRequired(), Length(max=100)])
    state = StringField('State/Province', validators=[DataRequired(), Length(max=100)])
    pincode = StringField('Postal/Zip Code', validators=[DataRequired(), Length(max=20)])
    
    # Contact Information
    contact_phone = StringField('Contact Phone', validators=[DataRequired(), Length(max=20)])
    contact_whatsapp = StringField('WhatsApp Number (optional)', validators=[Optional(), Length(max=20)])
    contact_email = StringField('Contact Email', validators=[Optional(), Email(), Length(max=120)])
    
    # Business Hours
    opening_time = StringField('Opening Time (e.g., 09:00)', 
                             validators=[DataRequired(), Length(min=5, max=5)])
    closing_time = StringField('Closing Time (e.g., 21:00)', 
                             validators=[DataRequired(), Length(min=5, max=5)])
    
    # Delivery Settings
    is_delivery_available = BooleanField('Offer Delivery Service', default=True)
    is_pickup_available = BooleanField('Allow Pickup', default=True)
    is_cod_available = BooleanField('Accept Cash on Delivery', default=True)
    delivery_radius_km = FloatField('Delivery Radius (km)', 
                                  validators=[Optional(), NumberRange(min=0)],
                                  default=5.0)
    delivery_charge = FloatField('Delivery Charge', 
                               validators=[Optional(), NumberRange(min=0)],
                               default=0.0)
    min_order_amount = FloatField('Minimum Order Amount', 
                                validators=[Optional(), NumberRange(min=0)],
                                default=0.0)
    
    # Shop Status
    is_active = BooleanField('Shop Active', default=True, 
                           description='Set shop as active or inactive')
    
    # Payment Information
    preferred_payment_method = SelectField('Preferred Payment Method',
                                        choices=[
                                            ('upi', 'UPI Payment'),
                                            ('bank_transfer', 'Bank Transfer'),
                                            ('both', 'Both UPI and Bank Transfer')
                                        ],
                                        default='upi')
    
    # UPI Payment Details
    upi_id = StringField('UPI ID (e.g., username@upi)', 
                        validators=[Optional(), Length(max=50)])
    upi_qr_code = FileField('Upload UPI QR Code', 
                           validators=[
                               FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Only image files are allowed')
                           ])
    
    # Bank Transfer Details
    bank_name = StringField('Bank Name', validators=[Optional(), Length(max=100)])
    account_holder_name = StringField('Account Holder Name', 
                                     validators=[Optional(), Length(max=100)])
    account_number = StringField('Account Number', 
                                validators=[
                                    Optional(),
                                    Length(min=9, max=18),
                                    Regexp('^[0-9]+$', message='Account number must contain only numbers')
                                ])
    ifsc_code = StringField('IFSC Code', 
                           validators=[
                               Optional(),
                               Length(min=11, max=11),
                               Regexp('^[A-Za-z]{4}0[A-Z0-9]{6}$', 
                                     message='Invalid IFSC code format. Example: HDFC0001234')
                           ])
    
    def validate_contact_whatsapp(self, field):
        if field.data and not field.data.startswith('+'):
            field.data = '+91' + field.data  # Default to India country code if not provided
    
    def validate(self, **kwargs):
        # Run the parent class validation first
        if not super().validate():
            return False
            
        # Validate payment method specific fields
        if self.preferred_payment_method.data in ['upi', 'both']:
            if not self.upi_id.data and not self.upi_qr_code.data:
                self.upi_id.errors.append('Either UPI ID or QR Code is required for UPI payments')
                return False
                
        if self.preferred_payment_method.data in ['bank_transfer', 'both']:
            required_fields = [
                (self.bank_name, 'Bank name is required for bank transfer'),
                (self.account_holder_name, 'Account holder name is required for bank transfer'),
                (self.account_number, 'Account number is required for bank transfer'),
                (self.ifsc_code, 'IFSC code is required for bank transfer')
            ]
            
            for field, error_msg in required_fields:
                if not field.data:
                    field.errors.append(error_msg)
                    return False
                    
        return True

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    category = StringField('Category', validators=[Optional(), Length(max=50)])
    image = FileField('Product Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')])

class ServiceForm(FlaskForm):
    name = StringField('Service Name', validators=[DataRequired(), Length(min=2, max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    duration = StringField('Duration', validators=[Optional(), Length(max=50)])
    category = StringField('Category', validators=[Optional(), Length(max=50)])
    image = FileField('Service Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')])

class CheckoutForm(FlaskForm):
    # Delivery Information
    delivery_option = SelectField('Delivery Option', 
                                choices=[
                                    ('delivery', 'Home Delivery'),
                                    ('pickup', 'Pickup from Shop')
                                ], 
                                validators=[DataRequired()])
    
    # Shipping Address (only required for delivery)
    shipping_address = TextAreaField('Delivery Address', 
                                   validators=[
                                       DataRequired(message='Please enter a delivery address'),
                                       Length(max=500)
                                   ],
                                   render_kw={
                                       'placeholder': 'Full delivery address including landmark',
                                       'rows': 3
                                   })
    
    # Location Details
    shipping_city = StringField('City', validators=[DataRequired(), Length(max=100)])
    shipping_state = StringField('State/Province', validators=[DataRequired(), Length(max=100)])
    shipping_pincode = StringField('Postal/Zip Code', 
                                 validators=[
                                     DataRequired(), 
                                     Length(min=3, max=20),
                                     Regexp(r'^[0-9-]+$', message='Invalid postal code format')
                                 ])
    
    # Contact Information
    shipping_phone = StringField('Contact Phone', 
                               validators=[
                                   DataRequired(), 
                                   Length(min=10, max=20),
                                   Regexp(r'^[0-9+\-\s()]+$', message='Invalid phone number')
                               ])
    
    # Payment Method
    payment_method = SelectField(
        'Payment Method', 
        choices=[
            ('cod', 'Cash on Delivery'), 
            ('qr', 'QR Code (UPI)'), 
            ('card', 'Credit/Debit Card'),
            ('wallet', 'Wallet')
        ], 
        validators=[DataRequired()]
    )
    
    # Order Notes
    notes = TextAreaField('Special Instructions (optional)', 
                         validators=[Optional(), Length(max=500)],
                         render_kw={
                             'placeholder': 'Any special delivery instructions or notes for the shop',
                             'rows': 2
                         })
    
    # Terms and Conditions
    terms_accepted = BooleanField(
        'I agree to the terms and conditions',
        validators=[DataRequired(message='You must accept the terms and conditions')]
    )
    
    def validate(self, **kwargs):
        # Run standard validation first
        if not super().validate():
            return False
            
        # Additional validation for delivery options
        if self.delivery_option.data == 'delivery':
            if not all([self.shipping_address.data, self.shipping_city.data, 
                       self.shipping_state.data, self.shipping_pincode.data]):
                self.delivery_option.errors.append('Please provide complete delivery address')
                return False
                
        # Validate phone number format
        if not any(c.isdigit() for c in self.shipping_phone.data):
            self.shipping_phone.errors.append('Please enter a valid phone number')
            return False
            
        return True


class ReviewForm(FlaskForm):
    """Form for submitting product/shop reviews."""
    RATING_CHOICES = [
        (5, '⭐⭐⭐⭐⭐ - Excellent'),
        (4, '⭐⭐⭐⭐ - Very Good'),
        (3, '⭐⭐⭐ - Good'),
        (2, '⭐⭐ - Fair'),
        (1, '⭐ - Poor')
    ]
    
    rating = SelectField('Your Rating', 
                        choices=RATING_CHOICES, 
                        coerce=int,
                        validators=[DataRequired()],
                        render_kw={
                            'class': 'form-select',
                            'aria-label': 'Select rating'
                        })
    
    title = StringField('Review Title', 
                       validators=[
                           DataRequired(),
                           Length(max=100)
                       ],
                       render_kw={
                           'placeholder': 'Brief summary of your experience',
                           'maxlength': '100'
                       })
    
    comment = TextAreaField('Your Review',
                          validators=[
                              DataRequired(),
                              Length(min=10, max=1000)
                          ],
                          render_kw={
                              'rows': 5,
                              'placeholder': 'Share details about your experience...',
                              'maxlength': '1000'
                          })
    
    is_anonymous = BooleanField('Post as Anonymous', default=False)
    
    def validate_rating(self, field):
        if field.data not in [1, 2, 3, 4, 5]:
            raise ValidationError('Please select a valid rating')
