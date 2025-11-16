# 🚀 SHOP&SERV - Quick Start Guide

## ⚡ Fast Setup (5 Minutes)

### Step 1: Install Dependencies
```bash
cd D:\SHO&SERV
pip install -r requirements.txt
```

### Step 2: Configure Environment
Edit the `.env` file and add your credentials:

**Required for Email (OTP/Password Reset):**
- Get Gmail App Password: https://myaccount.google.com/apppasswords
- Update `MAIL_USERNAME` and `MAIL_PASSWORD`

**Required for Payments:**
- Get Stripe Test Keys: https://dashboard.stripe.com/test/apikeys
- Update `STRIPE_PUBLIC_KEY` and `STRIPE_SECRET_KEY`

**Generate Secret Key:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```
Update `SECRET_KEY` in `.env`

### Step 3: Run the Application
```bash
python app.py
```

Or simply double-click `run.bat` on Windows!

### Step 4: Access the Application
Open your browser: **http://localhost:5000**

---

## 🔑 Default Login Credentials

**Admin Account:**
- Email: `admin@shopserv.com`
- Password: `admin123`

⚠️ **Change this password immediately after first login!**

---

## 🎯 Quick Test Flow

### Test as Customer:
1. Register a new customer account
2. Browse products
3. Add items to cart
4. Checkout and pay (use test card: 4242 4242 4242 4242)
5. View order history

### Test as Shop Owner:
1. Register as shop owner
2. Create your shop
3. Add products with images
4. View orders when customers purchase
5. Update order status

### Test as Admin:
1. Login with admin credentials
2. View dashboard statistics
3. Manage users, shops, and products
4. Monitor all orders

---

## 🧪 Stripe Test Cards

| Card Number | Result |
|-------------|--------|
| 4242 4242 4242 4242 | Success |
| 4000 0000 0000 0002 | Decline |

Use any future date for expiry and any 3-digit CVC.

---

## ❓ Troubleshooting

**Email not sending?**
- Verify Gmail App Password (not regular password)
- Enable 2FA on Gmail first
- Check MAIL_USERNAME and MAIL_PASSWORD in .env

**Payment not working?**
- Verify Stripe test keys are correct
- Check browser console for errors
- Ensure JavaScript is enabled

**Database errors?**
```bash
# Delete and recreate database
del shopserv.db
python app.py
```

---

## 📁 Project Structure Overview

```
D:\SHO&SERV\
├── app.py              # Main application (START HERE)
├── models.py           # Database models
├── forms.py            # Form definitions
├── config.py           # Configuration
├── .env                # Your credentials (EDIT THIS)
├── requirements.txt    # Dependencies
├── templates/          # HTML templates
├── static/
│   ├── css/           # Stylesheets
│   ├── js/            # JavaScript
│   └── uploads/       # User uploads
└── README.md          # Full documentation
```

---

## 🎓 Features Checklist

- ✅ User Authentication (Login/Register/Logout)
- ✅ Forgot Password with OTP
- ✅ Role-based Access (Customer/Shop Owner/Admin)
- ✅ Product Management (CRUD)
- ✅ Shopping Cart
- ✅ Checkout & Payment (Stripe)
- ✅ Order Management
- ✅ Email Notifications
- ✅ Admin Dashboard
- ✅ Responsive Design
- ✅ Security (CSRF, Password Hashing)
- ✅ Image Upload & Optimization

---

## 🌐 Deployment Ready

This application is ready to deploy to:
- Render
- Heroku
- PythonAnywhere
- Any platform supporting Flask

See README.md for deployment instructions.

---

## 💡 Tips

1. **For College Demo:** Use test Stripe keys and demo email
2. **For Production:** Get real Stripe keys and proper email service
3. **Security:** Always change default admin password
4. **Performance:** Use PostgreSQL for production (not SQLite)

---

**Need Help?** Check README.md for detailed documentation.

**Ready to Start?** Run `python app.py` and visit http://localhost:5000

---

Built with ❤️ for SHOP&SERV
