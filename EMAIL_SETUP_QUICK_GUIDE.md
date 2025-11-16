# 📧 Quick Email Setup Guide - Real OTP Delivery

## 🚀 Quick Setup (5 Minutes)

### Step 1: Get Gmail App Password

1. **Go to Google Account Settings**
   - Visit: https://myaccount.google.com/security
   - Or click your profile picture → "Manage your Google Account" → "Security"

2. **Enable 2-Step Verification** (if not already enabled)
   - Scroll to "Signing in to Google"
   - Click "2-Step Verification"
   - Follow the setup wizard

3. **Generate App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Select app: **Mail**
   - Select device: **Other (Custom name)**
   - Enter name: **SHOPSERV**
   - Click **Generate**
   - **Copy the 16-character password** (example: `abcd efgh ijkl mnop`)

### Step 2: Run Automated Setup

Open terminal in your project folder and run:

```bash
python setup_email.py
```

Follow the prompts:
1. Enter your Gmail address (e.g., `yourname@gmail.com`)
2. Paste the 16-character App Password
3. Enter a test email address
4. Confirm to save settings

The script will:
- ✅ Test your email credentials
- ✅ Send a test email
- ✅ Update your .env file automatically
- ✅ Confirm everything works

### Step 3: Restart Your Application

```bash
python app.py
```

That's it! OTP emails will now be sent to registered users.

---

## 🔧 Manual Setup (Alternative)

If you prefer to configure manually:

1. Open `.env` file in your project root
2. Update these lines:

```env
MAIL_USERNAME=your-actual-email@gmail.com
MAIL_PASSWORD=abcdefghijklmnop
MAIL_DEFAULT_SENDER=your-actual-email@gmail.com
```

3. Replace:
   - `your-actual-email@gmail.com` with your Gmail address
   - `abcdefghijklmnop` with your 16-character App Password (no spaces)

4. Save the file and restart your application

---

## ✅ Testing

1. Go to your application
2. Click "Forgot Password"
3. Enter a registered email address
4. Check your email inbox
5. You should receive an OTP within seconds

---

## 🆘 Troubleshooting

### "Authentication failed" error:
- ✓ Make sure you're using App Password, not your regular Gmail password
- ✓ Remove all spaces from the App Password
- ✓ Verify 2-Step Verification is enabled
- ✓ Try generating a new App Password

### Email not received:
- ✓ Check spam/junk folder
- ✓ Wait 1-2 minutes
- ✓ Verify the email address is correct
- ✓ Check if Gmail account has sending limits

### "Email service not configured" message:
- ✓ Make sure .env file is updated
- ✓ Restart your Flask application
- ✓ Check if .env is in the project root folder

---

## 🔒 Security Notes

- ✅ App Password is safer than your regular password
- ✅ .env file is in .gitignore (never committed to Git)
- ✅ You can revoke App Password anytime from Google Account
- ✅ Each app should have its own App Password

---

## 📊 What Happens After Setup

When a user clicks "Forgot Password":

1. User enters their registered email
2. System generates a 6-digit OTP
3. **Email is sent immediately** to their inbox
4. OTP is valid for 5 minutes
5. User enters OTP to verify
6. User can reset their password

**No demo mode, no fallback - Real email delivery!**

---

## 💡 Pro Tips

1. **Use a dedicated email** for your application (e.g., `shopserv2024@gmail.com`)
2. **Keep App Password secure** - treat it like a password
3. **Monitor email sending** - Gmail has daily sending limits
4. **Test regularly** to ensure emails are working

---

## 📞 Need Help?

- Gmail App Password Help: https://support.google.com/accounts/answer/185833
- Gmail Sending Limits: https://support.google.com/mail/answer/22839

---

## ✨ Ready to Go!

Once configured, your OTP system will:
- ✅ Send real emails instantly
- ✅ Work with any Gmail account
- ✅ Be production-ready
- ✅ Be secure and reliable

**Run `python setup_email.py` now to get started!**
