# OTP Setup Guide - Email & SMS Configuration

## Overview
The SHOP&SERV platform now supports sending OTP via both **Email** and **SMS** for password reset functionality.

---

## 📧 Email Configuration (Gmail)

### Step 1: Enable 2-Step Verification
1. Go to your Google Account: https://myaccount.google.com/
2. Click on **Security** in the left sidebar
3. Under "Signing in to Google", enable **2-Step Verification**

### Step 2: Generate App Password
1. Go to: https://myaccount.google.com/apppasswords
2. Select **Mail** as the app
3. Select **Other (Custom name)** as the device
4. Enter "SHOPSERV" as the name
5. Click **Generate**
6. Copy the 16-character password (remove spaces)

### Step 3: Update .env File
Open your `.env` file and update:
```env
MAIL_USERNAME=your-actual-email@gmail.com
MAIL_PASSWORD=your-16-character-app-password
MAIL_DEFAULT_SENDER=your-actual-email@gmail.com
```

**Example:**
```env
MAIL_USERNAME=shopserv2024@gmail.com
MAIL_PASSWORD=abcd efgh ijkl mnop
MAIL_DEFAULT_SENDER=shopserv2024@gmail.com
```

---

## 📱 SMS Configuration (Fast2SMS)

### Step 1: Create Fast2SMS Account
1. Go to: https://www.fast2sms.com/
2. Click **Sign Up** and create an account
3. Verify your mobile number

### Step 2: Get API Key
1. Login to your Fast2SMS dashboard
2. Go to **Dev API** section
3. Copy your **API Key**

### Step 3: Add Credits (Optional)
- Fast2SMS provides free test credits
- For production, purchase credits from the dashboard

### Step 4: Update .env File
Open your `.env` file and add:
```env
FAST2SMS_API_KEY=your-fast2sms-api-key-here
```

**Example:**
```env
FAST2SMS_API_KEY=ABCDefgh123456789XYZ
```

---

## 🔧 Testing the Setup

### Test Email OTP:
1. Make sure your `.env` has valid Gmail credentials
2. Go to Forgot Password page
3. Enter a registered email address
4. Check your email inbox for OTP

### Test SMS OTP:
1. Make sure your `.env` has valid Fast2SMS API key
2. Go to Forgot Password page
3. Enter a registered email (user must have phone number)
4. Check your mobile for SMS with OTP

---

## 🚀 How It Works

When a user requests password reset:

1. **Both Email & SMS**: If both are configured, OTP is sent via both channels
2. **Email Only**: If only email is configured, OTP is sent via email
3. **SMS Only**: If only SMS is configured, OTP is sent via SMS
4. **Fallback Mode**: If neither is configured, OTP is displayed on screen (for testing)

---

## 📝 Current Configuration Status

Check your terminal/console output when testing:
- ✅ "Email sent successfully to..." - Email is working
- ✅ "SMS sent successfully to..." - SMS is working
- ❌ "Email credentials not configured" - Email needs setup
- ❌ "SMS API key not configured" - SMS needs setup

---

## 🔒 Security Notes

1. **Never commit .env file** - It's in .gitignore for security
2. **Use App Passwords** - Never use your actual Gmail password
3. **Rotate API Keys** - Change keys periodically
4. **Monitor Usage** - Check Fast2SMS dashboard for SMS usage

---

## 🆘 Troubleshooting

### Email Not Sending:
- ✓ Check if 2-Step Verification is enabled
- ✓ Verify App Password is correct (no spaces)
- ✓ Check if "Less secure app access" is NOT needed (use App Password instead)
- ✓ Verify MAIL_USERNAME and MAIL_DEFAULT_SENDER are the same

### SMS Not Sending:
- ✓ Check if Fast2SMS API key is valid
- ✓ Verify you have SMS credits
- ✓ Check if phone number is in correct format (10 digits for India)
- ✓ Verify Fast2SMS account is active

### OTP Not Received:
- ✓ Check spam/junk folder for emails
- ✓ Wait 1-2 minutes for SMS delivery
- ✓ Verify the registered email/phone is correct
- ✓ Check console logs for error messages

---

## 📞 Support

For Fast2SMS support: https://www.fast2sms.com/support
For Gmail support: https://support.google.com/mail

---

## 🎯 Quick Start (For Testing)

If you want to test immediately without configuring email/SMS:

1. Leave email/SMS credentials as placeholders in `.env`
2. Try forgot password
3. **OTP will be displayed on screen** in the flash message
4. Copy the OTP and use it to reset password

This fallback mode is perfect for development and testing!
