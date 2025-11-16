# 🚀 SHOP&SERV - Complete Setup Guide

## 📋 Prerequisites

Before you begin, ensure you have:
- ✅ Python 3.8 or higher installed
- ✅ pip (Python package manager)
- ✅ A Gmail account (for OTP emails)
- ✅ Stripe account (optional, for card payments)

---

## 🔧 Step-by-Step Setup

### Step 1: Install Dependencies

Open terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install all required packages:
- Flask (web framework)
- Flask-SQLAlchemy (database ORM)
- Flask-Login (authentication)
- Flask-WTF (forms with CSRF protection)
- Werkzeug (password hashing)
- Pillow (image processing)
- Stripe (payment processing)
- qrcode (QR code generation)

---

### Step 2: Configure Environment Variables

1. **Copy the example file:**
   ```bash
   copy .env.example .env
   ```

2. **Edit `.env` file with your settings:**

```env
# Generate a random secret key (required)
SECRET_KEY=your-super-secret-key-change-this-now

# Stripe Configuration (optional for testing)
STRIPE_PUBLIC_KEY=pk_test_your_stripe_public_key
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key

# UPI Configuration for QR Payments
UPI_ID=yourmerchant@upi

# Email Configuration (required for OTP)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

---

### Step 3: Gmail App Password Setup

**Important:** Gmail requires an "App Password" for SMTP access.

1. **Enable 2-Factor Authentication:**
   - Go to: https://myaccount.google.com/security
   - Enable 2-Step Verification

2. **Generate App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and "Other (Custom name)"
   - Name it "SHOPSERV"
   - Copy the 16-character password
   - Paste it in `.env` as `MAIL_PASSWORD`

**Note:** Use the app password, NOT your regular Gmail password!

---

### Step 4: Stripe Setup (Optional)

If you want to test card payments:

1. **Create Stripe Account:**
   - Go to: https://stripe.com
   - Sign up for free

2. **Get Test API Keys:**
   - Go to: https://dashboard.stripe.com/test/apikeys
   - Copy "Publishable key" → `STRIPE_PUBLIC_KEY`
   - Copy "Secret key" → `STRIPE_SECRET_KEY`

3. **Test Card:**
   - Card Number: `4242 4242 4242 4242`
   - Expiry: Any future date
   - CVC: Any 3 digits

---

### Step 5: Initialize Database

Run the application once to create the database:

```bash
python app.py
```

The application will:
- ✅ Create `shop_serv.db` (SQLite database)
- ✅ Create all tables automatically
- ✅ Create upload directories
- ✅ Start the development server

You should see:
```
* Running on http://127.0.0.1:5000
```

---

### Step 6: Create Admin User (First Time Only)

The admin account uses static credentials:
- **Username:** `admin`
- **Password:** `ADMIN123`

However, you need to create the admin user in the database first.

**Option 1: Using Python Shell**

```bash
python
```

Then run:
```python
from app import app, db
from app.models.models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Check if admin exists
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        admin = User(
            email='admin@shopserv.com',
            full_name='System Administrator',
            role='admin',
            is_active=True
        )
        admin.set_password('ADMIN123')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
    else:
        print("Admin user already exists!")
```

Press `Ctrl+D` (or `Ctrl+Z` on Windows) to exit Python shell.

**Option 2: The admin will be auto-created on first login attempt**

---

## 🧪 Testing the Application

### Test as Customer

1. **Register:**
   - Go to: http://localhost:5000/register
   - Fill in details and select "Customer"
   - Click Register

2. **Verify Email (if OTP enabled):**
   - Check your email for OTP
   - Enter the 6-digit code
   - OTP expires in 5 minutes

3. **Browse Products:**
   - Click "Products" in navigation
   - Search and filter products
   - View product details

4. **Browse Services:**
   - Click "Services" in navigation
   - Search and filter services
   - View service details

5. **Add to Cart:**
   - Click "Add to Cart" on any product/service
   - View cart icon badge update

6. **Checkout:**
   - Go to Cart
   - Click "Proceed to Checkout"
   - Fill in shipping details
   - **Select Payment Method:**
     - **COD:** Order confirmed immediately
     - **QR Code:** Scan with UPI app, confirm payment
     - **Stripe:** Use test card `4242 4242 4242 4242`

7. **View Orders:**
   - Go to Dashboard
   - Click "My Orders"
   - View order status and details

---

### Test as Shop Owner

1. **Register:**
   - Go to: http://localhost:5000/register
   - Select "Shop Owner"
   - Complete registration

2. **Create Shop:**
   - After login, you'll be prompted to create a shop
   - Fill in shop name, description, address
   - Upload logo (optional)

3. **Add Products:**
   - Go to "My Shop" → "Add Product"
   - Fill in product details
   - Upload product image
   - Set price and stock

4. **Add Services:**
   - Go to "Manage Services" → "Add Service"
   - Fill in service details
   - Set duration (e.g., "1 hour")
   - Upload service image

5. **Manage Orders:**
   - View incoming orders
   - Update order status
   - See payment method (COD/QR/Stripe)

---

### Test as Admin

1. **Login:**
   - Go to: http://localhost:5000/login
   - Username: `admin`
   - Password: `ADMIN123`

2. **Manage Users:**
   - View all customers and shop owners
   - Activate/deactivate accounts
   - Monitor user activity

3. **Manage Shops:**
   - View all shops
   - Approve/reject shops
   - Activate/deactivate shops

4. **Manage Products & Services:**
   - View all products across all shops
   - View all services across all shops
   - Activate/deactivate listings

5. **Monitor Orders:**
   - View all orders system-wide
   - Track payment status
   - Monitor revenue

---

## 🔍 Troubleshooting

### Database Issues

**Problem:** Database errors or missing tables

**Solution:**
```bash
# Delete the database and recreate
del shop_serv.db  # Windows
rm shop_serv.db   # Mac/Linux

# Run app again to recreate
python app.py
```

---

### Email Not Sending

**Problem:** OTP emails not arriving

**Solutions:**
1. Check Gmail App Password is correct
2. Verify 2FA is enabled on Gmail
3. Check spam folder
4. Try different email provider
5. Check `.env` file has correct settings

**Test Email Configuration:**
```python
from app import app
from utils import send_email

with app.app_context():
    send_email(
        'your-email@gmail.com',
        'Test Email',
        'If you receive this, email is working!'
    )
```

---

### Stripe Payment Issues

**Problem:** Card payment not working

**Solutions:**
1. Verify Stripe keys are in test mode (start with `pk_test_` and `sk_test_`)
2. Use test card: `4242 4242 4242 4242`
3. Check Stripe dashboard for errors
4. Ensure Stripe library is installed: `pip install stripe`

---

### Image Upload Issues

**Problem:** Images not uploading

**Solutions:**
1. Check `static/uploads/` directory exists
2. Verify file size is under 2MB
3. Use supported formats: JPG, PNG, GIF, WEBP
4. Check file permissions on uploads folder

---

### Port Already in Use

**Problem:** `Address already in use` error

**Solution:**
```bash
# Windows - Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <process_id> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

Or run on different port:
```python
# In app.py, change the last line to:
app.run(debug=True, port=5001)
```

---

## 🎯 Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Edit .env with your settings
notepad .env

# Run application
python app.py

# Access application
# Open browser: http://localhost:5000
```

---

## 📁 Project Structure

```
SHOP&SERV/
├── app.py                    # Main application file
├── models.py                 # Database models
├── forms.py                  # WTForms definitions
├── utils.py                  # Helper functions
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this)
├── .env.example             # Environment template
├── shop_serv.db             # SQLite database (auto-created)
│
├── static/
│   ├── css/
│   │   └── style.css        # Main stylesheet
│   ├── js/
│   │   └── main.js          # JavaScript functions
│   └── uploads/
│       ├── products/        # Product images
│       ├── services/        # Service images
│       └── shops/           # Shop logos
│
└── templates/
    ├── base.html            # Base template
    ├── index.html           # Homepage
    ├── login.html           # Login page
    ├── register.html        # Registration
    ├── products.html        # Products listing
    ├── services.html        # Services listing
    ├── cart.html            # Shopping cart
    ├── checkout.html        # Checkout page
    ├── payment.html         # Stripe payment
    ├── payment_qr.html      # QR code payment
    └── shop/                # Shop owner templates
        ├── dashboard.html
        ├── products.html
        ├── services.html
        └── ...
```

---

## 🔐 Security Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Set `DEBUG=False` in production
- [ ] Use environment variables for all sensitive data
- [ ] Enable HTTPS
- [ ] Set up proper database backups
- [ ] Configure firewall rules
- [ ] Use production-grade database (PostgreSQL/MySQL)
- [ ] Set up proper logging
- [ ] Configure rate limiting
- [ ] Review and update CORS settings
- [ ] Set secure cookie flags
- [ ] Implement proper error handling

---

## 📚 Additional Resources

- **Flask Documentation:** https://flask.palletsprojects.com/
- **SQLAlchemy Docs:** https://docs.sqlalchemy.org/
- **Stripe API Docs:** https://stripe.com/docs/api
- **Python QR Code:** https://pypi.org/project/qrcode/

---

## 🎓 Learning Path

1. **Understand the basics:**
   - Flask routing and views
   - Jinja2 templating
   - SQLAlchemy models

2. **Explore authentication:**
   - Flask-Login integration
   - Password hashing
   - Session management

3. **Study payment integration:**
   - Stripe API
   - QR code generation
   - Payment webhooks

4. **Master the frontend:**
   - Responsive CSS
   - JavaScript fetch API
   - Form validation

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Application starts without errors
- [ ] Database is created with all tables
- [ ] Can register new users
- [ ] OTP emails are received
- [ ] Can login as customer
- [ ] Can login as shop owner
- [ ] Can login as admin (admin/ADMIN123)
- [ ] Can create shop
- [ ] Can add products
- [ ] Can add services
- [ ] Can add items to cart
- [ ] Can checkout with COD
- [ ] Can checkout with QR code
- [ ] Can checkout with Stripe (if configured)
- [ ] Images upload successfully
- [ ] Orders are created correctly
- [ ] Notifications work
- [ ] All pages are responsive

---

**🎉 Congratulations! Your SHOP&SERV platform is ready!**

For questions or issues, check the documentation files:
- `START_HERE.md` - Quick start guide
- `FEATURES_SUMMARY.md` - Complete features list
- `TESTING_GUIDE.md` - Testing procedures
- `README.md` - Full documentation
