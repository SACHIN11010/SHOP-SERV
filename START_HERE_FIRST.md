# 🚀 START HERE FIRST - SHOP&SERV Quick Guide

## ⚡ Get Started in 3 Steps

### Step 1: Install Dependencies (2 minutes)
```bash
pip install -r requirements.txt
```

### Step 2: Configure Email (1 minute)
Edit `.env` file and add your Gmail credentials:
```env
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

**How to get Gmail App Password:**
1. Go to https://myaccount.google.com/security
2. Enable 2-Step Verification
3. Click "App passwords"
4. Generate password for "Mail" + "Windows Computer"
5. Copy the 16-character password

### Step 3: Start Application (30 seconds)
```bash
python app.py
```

**Then open:** http://localhost:5000

---

## 🎯 First Login

### Admin Login (Two Options)

**Option 1 - Quick Admin:**
- Username: `admin`
- Password: `ADMIN123`

**Option 2 - Email Admin:**
- Email: `admin@shopserv.com`
- Password: `admin123`

---

## 📖 What to Read Next

1. **QUICK_START.md** - 5-minute complete setup guide
2. **README.md** - Full documentation
3. **FEATURE_CHECKLIST.md** - All 200+ features
4. **PROJECT_COMPLETE.md** - Project summary

---

## 🎬 Quick Demo Workflow

### 1. Test Customer Flow (5 minutes)
1. Click "Register" → Choose "Customer"
2. Create account and login
3. Browse products
4. Add to cart
5. Checkout with COD

### 2. Test Shop Owner Flow (5 minutes)
1. Logout → Register as "Shop Owner"
2. Login and create shop
3. Add 2-3 products
4. View dashboard

### 3. Test Admin Flow (2 minutes)
1. Logout → Login as admin
2. View dashboard
3. See all users, shops, products

---

## ⚙️ Optional Configuration

### Stripe Payment (Optional)
Add to `.env`:
```env
STRIPE_PUBLIC_KEY=pk_test_your_key
STRIPE_SECRET_KEY=sk_test_your_key
```
Get keys from: https://dashboard.stripe.com/test/apikeys

### UPI QR Code (Optional)
Add to `.env`:
```env
UPI_ID=yourname@upi
```

---

## 🆘 Quick Troubleshooting

### Problem: Email not sending
**Solution:** Check Gmail app password (not regular password)

### Problem: Database error
**Solution:** Delete `shopserv.db` and restart `python app.py`

### Problem: Port in use
**Solution:** Change port in `app.py` line 1113 to 5001

### Problem: Module not found
**Solution:** Run `pip install -r requirements.txt`

---

## 📁 Important Files

- **app.py** - Main application
- **.env** - Your configuration
- **requirements.txt** - Dependencies
- **README.md** - Full documentation

---

## ✅ What's Included

✅ Customer registration & shopping
✅ Shop owner product management
✅ Admin dashboard
✅ 3 payment methods (COD, QR, Stripe)
✅ Email OTP system
✅ Modern responsive UI
✅ Complete security

---

## 🎉 You're Ready!

Run this command and start exploring:
```bash
python app.py
```

**Access at:** http://localhost:5000

---

**Need help? Check README.md or QUICK_START.md**
