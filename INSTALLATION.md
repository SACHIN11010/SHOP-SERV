# 📦 SHOP&SERV - Complete Installation Guide

## 🎯 Prerequisites

Before you begin, ensure you have:

- **Python 3.8+** installed ([Download](https://www.python.org/downloads/))
- **pip** (comes with Python)
- **Git** (optional, for version control)
- **Gmail account** (for email functionality)
- **Stripe account** (for payment processing)

---

## 🚀 Installation Steps

### Step 1: Verify Python Installation

```bash
python --version
```

Should show Python 3.8 or higher.

### Step 2: Navigate to Project Directory

```bash
cd D:\SHO&SERV
```

### Step 3: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- SQLAlchemy (database ORM)
- Flask-Login (authentication)
- Flask-Mail (email)
- Stripe (payments)
- Pillow (image processing)
- And more...

### Step 5: Configure Environment Variables

Edit the `.env` file in the project root:

```env
SECRET_KEY=your-generated-secret-key-here
STRIPE_PUBLIC_KEY=pk_test_your_stripe_public_key
STRIPE_SECRET_KEY=sk_test_your_stripe_secret_key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

#### Generate Secret Key:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and use it as `SECRET_KEY`.

---

## 📧 Setting Up Gmail for Emails

### Step 1: Enable 2-Factor Authentication

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification**

### Step 2: Generate App Password

1. Go to [App Passwords](https://myaccount.google.com/apppasswords)
2. Select **Mail** and **Windows Computer** (or Other)
3. Click **Generate**
4. Copy the 16-character password (remove spaces)
5. Use this as `MAIL_PASSWORD` in `.env`

**Important:** Use the App Password, NOT your regular Gmail password!

---

## 💳 Setting Up Stripe for Payments

### Step 1: Create Stripe Account

1. Go to [Stripe](https://stripe.com)
2. Sign up for a free account
3. Verify your email

### Step 2: Get API Keys

1. Go to [Stripe Dashboard](https://dashboard.stripe.com)
2. Click **Developers** → **API keys**
3. Toggle **Test mode** ON (for development)
4. Copy **Publishable key** (starts with `pk_test_`)
5. Copy **Secret key** (starts with `sk_test_`)
6. Add them to `.env` file

**Test Mode:** Use test keys for development. No real money is charged.

---

## 🏃 Running the Application

### Method 1: Using Python Directly

```bash
python app.py
```

### Method 2: Using the Batch File (Windows)

Double-click `run.bat` or:

```bash
run.bat
```

### Method 3: Using Flask CLI

```bash
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```

### Access the Application

Open your browser and go to:
```
http://localhost:5000
```

or

```
http://127.0.0.1:5000
```

---

## 🔑 Default Login Credentials

### Admin Account
- **Email:** admin@shopserv.com
- **Password:** admin123

**⚠️ SECURITY WARNING:** Change this password immediately after first login!

---

## ✅ Verify Installation

Run the verification script:

```bash
python verify_setup.py
```

This checks if all required files are present.

---

## 🧪 Testing the Application

### Test as Customer

1. **Register:**
   - Click "Register"
   - Select "Customer"
   - Fill in details
   - Submit

2. **Browse Products:**
   - Click "Products"
   - Search or filter
   - View product details

3. **Shopping:**
   - Add items to cart
   - Go to cart
   - Proceed to checkout
   - Enter shipping info
   - Pay with test card: `4242 4242 4242 4242`
   - Any future expiry date
   - Any 3-digit CVC

4. **View Orders:**
   - Go to Dashboard
   - See order history

### Test as Shop Owner

1. **Register:**
   - Click "Register"
   - Select "Shop Owner"
   - Fill in details
   - Submit

2. **Create Shop:**
   - Login
   - Create shop profile
   - Upload logo (optional)

3. **Add Products:**
   - Go to "My Products"
   - Click "Add Product"
   - Fill in details
   - Upload image
   - Set price and stock

4. **Manage Orders:**
   - When customers buy
   - View in "Orders"
   - Update status

### Test as Admin

1. **Login:**
   - Email: admin@shopserv.com
   - Password: admin123

2. **Explore Dashboard:**
   - View statistics
   - Manage users
   - Manage shops
   - Manage products
   - View all orders

---

## 🐛 Troubleshooting

### Issue: "Module not found" error

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Email not sending

**Possible causes:**
- Wrong Gmail App Password
- 2FA not enabled
- Wrong email in .env

**Solution:**
1. Verify 2FA is enabled
2. Generate new App Password
3. Update .env file
4. Restart application

### Issue: Payment not working

**Possible causes:**
- Wrong Stripe keys
- Not in test mode
- JavaScript disabled

**Solution:**
1. Verify Stripe test keys
2. Check browser console for errors
3. Ensure JavaScript is enabled

### Issue: Database error

**Solution:**
```bash
# Delete database and restart
del shopserv.db
python app.py
```

### Issue: Port already in use

**Solution:**
```bash
# Use different port
python app.py --port 5001
```

Or kill the process using port 5000:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Issue: Images not uploading

**Solution:**
1. Check `static/uploads` directory exists
2. Verify file size < 16MB
3. Use supported formats: jpg, jpeg, png, gif, webp

---

## 📁 Project Structure

```
D:\SHO&SERV\
├── app.py                    # Main Flask application
├── models.py                 # Database models
├── forms.py                  # Form definitions
├── config.py                 # Configuration
├── utils.py                  # Utility functions
├── requirements.txt          # Dependencies
├── .env                      # Environment variables (YOUR CREDENTIALS)
├── .env.example             # Example environment file
├── .gitignore               # Git ignore rules
├── README.md                # Main documentation
├── QUICKSTART.md            # Quick start guide
├── FEATURES.md              # Feature list
├── INSTALLATION.md          # This file
├── setup.py                 # Setup script
├── verify_setup.py          # Verification script
├── run.bat                  # Windows run script
├── shopserv.db              # SQLite database (created on first run)
├── static/
│   ├── css/
│   │   └── style.css        # Main stylesheet
│   ├── js/
│   │   └── main.js          # JavaScript
│   └── uploads/             # User uploads
│       ├── products/        # Product images
│       └── shops/           # Shop logos
└── templates/
    ├── base.html            # Base template
    ├── index.html           # Homepage
    ├── login.html           # Login page
    ├── register.html        # Registration
    ├── products.html        # Products listing
    ├── cart.html            # Shopping cart
    ├── checkout.html        # Checkout
    ├── payment.html         # Payment
    ├── customer/            # Customer templates
    │   ├── dashboard.html
    │   └── profile.html
    ├── shop/                # Shop owner templates
    │   ├── dashboard.html
    │   ├── create_shop.html
    │   ├── edit_shop.html
    │   ├── products.html
    │   ├── add_product.html
    │   ├── edit_product.html
    │   └── orders.html
    ├── admin/               # Admin templates
    │   ├── dashboard.html
    │   ├── users.html
    │   ├── shops.html
    │   ├── products.html
    │   └── orders.html
    └── errors/              # Error pages
        ├── 404.html
        ├── 403.html
        └── 500.html
```

---

## 🔄 Updating Dependencies

To update all packages:

```bash
pip install --upgrade -r requirements.txt
```

To update specific package:

```bash
pip install --upgrade Flask
```

---

## 🌐 Deployment

### For Production Deployment:

1. **Use PostgreSQL instead of SQLite**
2. **Set environment variables on hosting platform**
3. **Use real Stripe keys (not test keys)**
4. **Enable HTTPS**
5. **Set `SESSION_COOKIE_SECURE = True`**
6. **Use production email service**
7. **Set `DEBUG = False`**

See README.md for detailed deployment instructions.

---

## 📞 Support

If you encounter issues:

1. Check this installation guide
2. Review error messages carefully
3. Check the troubleshooting section
4. Verify all environment variables
5. Ensure all dependencies are installed

---

## ✨ You're Ready!

If you've completed all steps:

1. ✅ Python installed
2. ✅ Dependencies installed
3. ✅ Environment configured
4. ✅ Gmail setup complete
5. ✅ Stripe setup complete
6. ✅ Application running

**You're ready to use SHOP&SERV!**

Visit: http://localhost:5000

---

**Happy Coding! 🚀**
