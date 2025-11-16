# 🚀 QUICK START GUIDE - SHOP&SERV

## ⚡ Fast Setup (5 Minutes)

### Step 1: Install Dependencies

```bash
cd D:\SHO&SERV
pip install -r requirements.txt
```

### Step 2: Configure Environment Variables

1. Copy the example environment file:
```bash
copy .env.example .env
```

2. Edit `.env` file with your credentials:
   - **For Email (OTP)**: Add Gmail credentials
   - **For Stripe**: Add test API keys
   - **For QR Payments**: Update UPI ID (optional)

**Minimum Required Configuration:**
```env
SECRET_KEY=your-secret-key-change-this
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### Step 3: Run the Application

```bash
python app.py
```

The application will:
- ✅ Create the database automatically
- ✅ Create upload folders
- ✅ Create default admin user
- ✅ Start on http://localhost:5000

### Step 4: Access the Application

Open your browser and go to: **http://localhost:5000**

---

## 👤 Default Login Credentials

### Admin Access
- **Email:** `admin@shopserv.com`
- **Password:** `admin123`

Or use the static admin login:
- **Username:** `admin`
- **Password:** `ADMIN123`

---

## 🎯 Quick Test Workflow

### 1. Register as Customer
1. Click "Register" → Select "Customer" role
2. Fill in details and submit
3. Login with your credentials

### 2. Register as Shop Owner
1. Click "Register" → Select "Shop Owner" role
2. Fill in details and submit
3. Login and create your shop
4. Add products/services

### 3. Test Shopping Flow
1. Login as customer
2. Browse products
3. Add to cart
4. Checkout
5. Choose payment method:
   - **COD** (instant)
   - **QR Code** (UPI)
   - **Stripe** (requires API keys)

### 4. Test Admin Features
1. Login as admin
2. View dashboard
3. Manage users, shops, products
4. View all orders

---

## 🔧 Troubleshooting

### Database Issues
If you encounter database errors:
```bash
# Delete and recreate database
del shopserv.db
python app.py
```

### Email Not Working
- Verify Gmail app password (not regular password)
- Enable 2-Factor Authentication on Gmail
- Generate app password from Google Account settings

### Stripe Not Working
- Use test mode keys (pk_test_... and sk_test_...)
- Get keys from https://dashboard.stripe.com/test/apikeys

### Port Already in Use
Change port in `app.py` (last line):
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001
```

---

## 📧 Setting Up Gmail App Password

1. Go to https://myaccount.google.com/security
2. Enable **2-Step Verification**
3. Go to **App passwords**
4. Select **Mail** and **Windows Computer**
5. Copy the 16-character password
6. Use this in `.env` as `MAIL_PASSWORD`

---

## 💳 Setting Up Stripe Test Mode

1. Create account at https://stripe.com
2. Go to **Developers** → **API keys**
3. Toggle **Test mode** ON
4. Copy:
   - **Publishable key** (starts with `pk_test_`)
   - **Secret key** (starts with `sk_test_`)
5. Add to `.env` file

**Test Card Numbers:**
- Success: `4242 4242 4242 4242`
- Decline: `4000 0000 0000 0002`
- Use any future date and any 3-digit CVC

---

## 🎨 Features Overview

### ✅ Customer Features
- Browse products and services
- Search and filter by category
- Add to cart
- Multiple payment options (COD, QR, Stripe)
- Order tracking
- Profile management

### ✅ Shop Owner Features
- Create and manage shop
- Add/edit/delete products and services
- Upload images
- Manage orders
- View sales analytics
- Update order status

### ✅ Admin Features
- User management
- Shop approval/management
- Product moderation
- Order monitoring
- Platform analytics
- Enable/disable users and shops

### ✅ Security Features
- Password hashing (Werkzeug)
- OTP verification (5-minute expiry)
- CSRF protection
- Role-based access control
- Secure file uploads
- Session management

---

## 📱 Payment Methods

### 1. Cash on Delivery (COD)
- No setup required
- Order confirmed immediately
- Pay when product is delivered

### 2. QR Code Payment (UPI)
- Dynamic QR code generated
- Scan with any UPI app
- Confirm payment after scanning

### 3. Online Payment (Stripe)
- Requires Stripe API keys
- Real-time payment processing
- Secure card payments

---

## 🌐 Production Deployment

### Before Deploying:
1. Change `SECRET_KEY` to a strong random string
2. Change admin password
3. Set `SESSION_COOKIE_SECURE = True` in `config.py`
4. Use PostgreSQL instead of SQLite
5. Set `debug=False` in `app.py`
6. Use production Stripe keys

### Deploy to Render/Heroku:
```bash
# Add gunicorn (already in requirements.txt)
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy to platform
git push heroku main
```

---

## 📞 Support

If you encounter issues:
1. Check this guide
2. Review error messages in terminal
3. Check `.env` configuration
4. Verify all dependencies are installed
5. Check `README.md` for detailed documentation

---

## ✨ Project Highlights

- ✅ **Production-ready** code structure
- ✅ **Modern UI** with animations
- ✅ **Fully responsive** design
- ✅ **Real payment** integration
- ✅ **Email/OTP** system
- ✅ **Role-based** access control
- ✅ **Secure** authentication
- ✅ **Complete CRUD** operations
- ✅ **Professional** documentation

---

**Ready to start? Run `python app.py` and visit http://localhost:5000** 🚀
