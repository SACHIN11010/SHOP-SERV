# 🔐 Complete Step-by-Step Guide: Forgot Password Setup

## ✅ Follow These Steps Exactly

---

## **STEP 1: Get Gmail App Password** (5 minutes)

### 1.1 Open Google Account Security
- Open your web browser
- Go to: **https://myaccount.google.com/security**
- Sign in with your Gmail account

### 1.2 Enable 2-Step Verification (if not already enabled)
- Scroll down to "Signing in to Google"
- Click on **"2-Step Verification"**
- Click **"Get Started"**
- Follow the steps to verify your phone number
- Complete the setup

### 1.3 Generate App Password
- Go to: **https://myaccount.google.com/apppasswords**
- You might need to sign in again
- Under "Select app", choose **"Mail"**
- Under "Select device", choose **"Other (Custom name)"**
- Type: **SHOPSERV**
- Click **"Generate"**
- You'll see a 16-character password like: `abcd efgh ijkl mnop`
- **COPY THIS PASSWORD** (you'll need it in the next step)

---

## **STEP 2: Run the Setup Script** (2 minutes)

### 2.1 Open Terminal/Command Prompt
- Press `Windows + R`
- Type: `cmd` and press Enter
- Navigate to your project folder:
  ```bash
  cd D:\SHO&SERV
  ```

### 2.2 Run the Setup Script
```bash
python setup_email.py
```

### 2.3 Follow the Prompts

**Prompt 1:** Enter your Gmail address
```
Email: youremail@gmail.com
```
(Replace with your actual Gmail)

**Prompt 2:** Enter your Gmail App Password
```
App Password: abcd efgh ijkl mnop
```
(Paste the 16-character password from Step 1.3)

**Prompt 3:** Enter a test email address
```
Test Email: youremail@gmail.com
```
(Use the same email or another email you can check)

**Prompt 4:** Save settings?
```
💾 Save these settings to .env file? (yes/no): yes
```

### 2.4 Check Results
- ✅ If successful, you'll see: "Email sent successfully!"
- ✅ Check your test email inbox
- ✅ You should receive a test email from SHOP&SERV

---

## **STEP 3: Restart Your Application** (1 minute)

### 3.1 Stop Current Application
- If your Flask app is running, press `Ctrl + C` in the terminal

### 3.2 Start Application Again
```bash
python app.py
```

Wait for the message:
```
* Running on http://127.0.0.1:5000
```

---

## **STEP 4: Test Forgot Password** (2 minutes)

### 4.1 Open Your Application
- Open browser
- Go to: **http://127.0.0.1:5000**

### 4.2 Go to Login Page
- Click **"Login"** button

### 4.3 Click Forgot Password
- Click **"Forgot Password?"** link

### 4.4 Enter Registered Email
- Enter an email address that's registered in your system
- Click **"Send OTP"**

### 4.5 Check Your Email
- Open your email inbox
- Look for email from SHOP&SERV
- Subject: "Password Reset OTP - SHOP&SERV"
- You'll see a 6-digit OTP code

### 4.6 Enter OTP
- Copy the 6-digit OTP from email
- Paste it in the OTP verification page
- Click **"Verify OTP"**

### 4.7 Reset Password
- Enter your new password
- Confirm the password
- Click **"Reset Password"**

### 4.8 Login with New Password
- Go to login page
- Use your email and new password
- Click **"Login"**

✅ **SUCCESS!** Your forgot password system is working!

---

## 🎯 Quick Checklist

Before you start, make sure you have:
- [ ] Gmail account
- [ ] Access to Google Account settings
- [ ] Terminal/Command Prompt access
- [ ] Flask application files in `D:\SHO&SERV`
- [ ] At least one registered user in your system

---

## 🆘 Troubleshooting

### Problem: "2-Step Verification not enabled"
**Solution:** 
- Go to https://myaccount.google.com/security
- Enable 2-Step Verification first
- Then generate App Password

### Problem: "Can't find App Passwords option"
**Solution:**
- Make sure 2-Step Verification is enabled
- Try this direct link: https://myaccount.google.com/apppasswords
- If still not visible, your account might have restrictions

### Problem: "Authentication failed" in setup script
**Solution:**
- Make sure you copied the App Password correctly
- Remove all spaces from the password
- Try generating a new App Password
- Use the password immediately (they can expire)

### Problem: "Email not received"
**Solution:**
- Check spam/junk folder
- Wait 1-2 minutes
- Verify the email address is registered in your system
- Check if Gmail has sending limits

### Problem: "Email service not configured" message
**Solution:**
- Make sure you ran `python setup_email.py`
- Check if `.env` file was updated
- Restart your Flask application
- Verify `.env` file is in project root folder

### Problem: Setup script not found
**Solution:**
- Make sure you're in the correct folder: `D:\SHO&SERV`
- Check if `setup_email.py` file exists
- Run: `dir setup_email.py` to verify

---

## 📋 Summary of Commands

```bash
# Navigate to project
cd D:\SHO&SERV

# Run setup script
python setup_email.py

# Restart application
python app.py
```

---

## 🔍 Verify Your Setup

After completing all steps, verify:

1. **Check .env file:**
   ```bash
   type .env | findstr MAIL
   ```
   Should show:
   ```
   MAIL_USERNAME=youremail@gmail.com
   MAIL_PASSWORD=your16charpassword
   MAIL_DEFAULT_SENDER=youremail@gmail.com
   ```

2. **Test email sending:**
   - Use forgot password feature
   - Should receive email within 30 seconds

3. **Check application logs:**
   - Look for: "Email sent successfully to..."
   - No errors about email configuration

---

## ⏱️ Total Time Required

- **Step 1:** 5 minutes (Gmail setup)
- **Step 2:** 2 minutes (Run script)
- **Step 3:** 1 minute (Restart app)
- **Step 4:** 2 minutes (Testing)

**Total: ~10 minutes** ⚡

---

## 🎉 What You'll Have After Setup

✅ Real-time OTP emails sent to users
✅ Professional password reset system
✅ Secure email delivery via Gmail
✅ Production-ready forgot password feature
✅ No demo mode or fallback

---

## 📞 Still Need Help?

If you're stuck on any step:

1. **Check the error message** - it usually tells you what's wrong
2. **Read the troubleshooting section** above
3. **Verify each step** was completed correctly
4. **Try the manual setup** method in `EMAIL_SETUP_QUICK_GUIDE.md`

---

## 🚀 Ready to Start?

**Begin with STEP 1 now!**

Open your browser and go to: **https://myaccount.google.com/security**

Good luck! 🎯
