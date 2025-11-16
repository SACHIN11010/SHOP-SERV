# 🔐 Gmail App Password Setup Guide for SHOP&SERV

## 📋 Overview
This guide will help you generate a new Gmail App Password for the SHOP&SERV email OTP system. **App Passwords are different from your regular Gmail password** and are required for applications to access your Gmail account securely.

## ⚠️ Important Security Notes
- **NEVER use your regular Gmail password** in the application
- App Passwords are **16-character codes** that give specific apps access to your account
- You **must have 2-Step Verification enabled** to use App Passwords
- Each App Password can only be used for **one application**
- **Store your App Password securely** - treat it like a master password

---

## 🚀 Step-by-Step Setup

### Step 1: Enable 2-Step Verification (Required)
1. Go to your Google Account: https://myaccount.google.com/
2. Click on **"Security"** in the left navigation panel
3. Find **"Signing in to Google"** section
4. Click on **"2-Step Verification"**
5. If it's off, click **"Get Started"** and follow the setup process
6. You'll need:
   - Your phone number (for verification codes)
   - A backup phone number (optional but recommended)
   - Backup codes (save these securely!)

### Step 2: Generate App Password
1. Stay on the **Security** page of your Google Account
2. In the **"Signing in to Google"** section, click **"App Passwords"**
   - If you don't see this option, make sure 2-Step Verification is enabled
3. You may need to sign in again with your Gmail password
4. On the App Passwords page:
   - Under **"Select app"**, choose **"Mail"**
   - Under **"Select device"**, choose **"Other (Custom name)"**
   - Enter a descriptive name: **"SHOP&SERV Email OTP"**
   - Click **"GENERATE"**

### Step 3: Copy Your App Password
1. Google will generate a **16-character password**
2. **Copy this password immediately** - it won't be shown again
3. The password format will be like: `xxxx xxxx xxxx xxxx` (4 groups of 4 characters)
4. **Remove the spaces** when using it in your application
5. Store it in a secure password manager

---

## 🔧 Configure SHOP&SERV

### Method 1: Using the Setup Script (Recommended)
1. Run the interactive setup script:
   ```bash
   python setup_email.py
   ```
2. Enter your Gmail address when prompted
3. Paste your 16-character App Password (spaces will be removed automatically)
4. The script will test the connection and update your `.env` file

### Method 2: Manual Configuration
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` file and update these lines:
   ```env
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-16-character-app-password-without-spaces
   MAIL_DEFAULT_SENDER=your-email@gmail.com
   ```

### Method 3: Using the Test Script
1. Test your configuration:
   ```bash
   python test_email_config.py --to your-test-email@example.com
   ```
2. This will validate your settings and send a test email

---

## 🔍 Troubleshooting

### Common Issues and Solutions

#### ❌ "Authentication failed" Error
**Causes:**
- Using regular Gmail password instead of App Password
- App Password typed incorrectly
- 2-Step Verification not enabled
- App Password revoked or expired

**Solutions:**
1. Double-check you're using the 16-character App Password
2. Generate a new App Password if unsure
3. Ensure 2-Step Verification is enabled
4. Remove all spaces from the App Password

#### ❌ "Invalid App Password" Error
**Causes:**
- App Password was revoked
- Too many failed login attempts
- Account security lock

**Solutions:**
1. Generate a fresh App Password
2. Wait 30 minutes if account is temporarily locked
3. Check Google Account security alerts

#### ❌ "Connection timed out" Error
**Causes:**
- Network connectivity issues
- Firewall blocking SMTP port 587
- Incorrect SMTP server settings

**Solutions:**
1. Check internet connection
2. Ensure port 587 is not blocked
3. Verify SMTP settings: `smtp.gmail.com:587`

#### ❌ "Less secure app access" Warning
**Note:** Google deprecated "Less secure app access". Always use App Passwords instead.

---

## 🔄 Managing App Passwords

### View Existing App Passwords
1. Go to: https://myaccount.google.com/apppasswords
2. You'll see all your active App Passwords
3. Each shows the app name and creation date

### Revoke an App Password
1. On the App Passwords page, find the password you want to revoke
2. Click **"Revoke"** next to the password
3. Confirm the revocation
4. **Important:** Update your application immediately with a new password

### Best Practices
- **Use descriptive names** for each App Password
- **Regularly review** your active App Passwords
- **Revoke unused** App Passwords immediately
- **Don't reuse** App Passwords across applications
- **Generate new passwords** if you suspect any security breach

---

## 🛡️ Security Best Practices

### Password Security
- ✅ Use App Passwords (never regular passwords)
- ✅ Store App Passwords in password managers
- ✅ Generate unique passwords for each application
- ✅ Regularly rotate App Passwords
- ❌ Never write passwords in code or commit to version control
- ❌ Never share App Passwords via email or chat
- ❌ Never use public computers to manage passwords

### Account Security
- ✅ Enable 2-Step Verification
- ✅ Use a strong, unique Gmail password
- ✅ Regularly review account activity
- ✅ Set up recovery phone and email
- ✅ Use hardware security keys if available

### Application Security
- ✅ Use environment variables for credentials
- ✅ Never commit `.env` files to version control
- ✅ Use HTTPS in production
- ✅ Implement proper logging and monitoring
- ✅ Regular security audits

---

## 📱 Alternative Email Providers

If you prefer not to use Gmail, SHOP&SERV supports:

### Outlook/Hotmail
```env
MAIL_PROVIDER=outlook
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-outlook-app-password
```

### Zoho Mail
```env
MAIL_PROVIDER=zoho
MAIL_SERVER=smtp.zoho.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@zoho.com
MAIL_PASSWORD=your-zoho-app-password
```

### SendGrid (Recommended for Production)
```env
MAIL_PROVIDER=sendgrid
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key
```

---

## 🆘 Getting Help

### Official Resources
- **Google App Passwords Help**: https://support.google.com/accounts/answer/185833
- **2-Step Verification Help**: https://support.google.com/accounts/answer/185839
- **Google Account Security**: https://myaccount.google.com/security

### SHOP&SERV Support
- **Test your configuration**: `python test_email_config.py`
- **Run setup wizard**: `python setup_email.py`
- **Check logs**: `logs/email_test.log`

### Emergency Steps
If you lose access to your Gmail account:
1. Use Google Account Recovery: https://accounts.google.com/signin/recovery
2. Contact your domain administrator (if using work/school account)
3. Generate new App Passwords after regaining access

---

## ✅ Quick Checklist

Before completing setup, verify:

- [ ] 2-Step Verification is enabled
- [ ] App Password generated (16 characters)
- [ ] App Password copied without spaces
- [ ] `.env` file updated with correct credentials
- [ ] Email configuration tested successfully
- [ ] Test email received
- [ ] Application restarted after configuration
- [ ] OTP functionality tested with real user account

---

**🎉 Congratulations!** Your SHOP&SERV email system is now securely configured with Gmail App Passwords.

**⚠️ Remember**: Keep your App Password secure and never share it with anyone!
