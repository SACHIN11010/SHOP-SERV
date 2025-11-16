# 🛡️ SHOP&SERV Security Best Practices & Warnings

## ⚠️ CRITICAL SECURITY WARNINGS

### 🚫 NEVER DO THESE THINGS
- **NEVER hardcode passwords in source code**
- **NEVER commit `.env` files to version control**
- **NEVER use your regular email password in applications**
- **NEVER share credentials via email, chat, or unencrypted channels**
- **NEVER use default passwords in production**
- **NEVER disable security features for convenience**
- **NEVER log passwords or sensitive data**
- **NEVER use the same password across multiple services**

### ✅ ALWAYS DO THESE THINGS
- **ALWAYS use App Passwords for email authentication**
- **ALWAYS store credentials in environment variables**
- **ALWAYS enable 2FA on all accounts**
- **ALWAYS use HTTPS in production**
- **ALWAYS validate and sanitize user inputs**
- **ALWAYS keep dependencies updated**
- **ALWAYS use strong, unique passwords**
- **ALWAYS backup your data securely**

---

## 🔐 Password Management

### Environment Variables
```bash
# ✅ GOOD: Use environment variables
MAIL_USERNAME=${MAIL_USERNAME}
MAIL_PASSWORD=${MAIL_PASSWORD}

# ❌ BAD: Hardcoded passwords
MAIL_USERNAME="myemail@gmail.com"
MAIL_PASSWORD="mypassword123"
```

### App Passwords vs Regular Passwords
| Feature | Regular Password | App Password |
|---------|------------------|--------------|
| Usage | Gmail login | Application access |
| Format | Your choice | 16 characters |
| Security | Risk of exposure | Limited scope |
| 2FA Required | Yes | Yes |
| Revocation | Affects all access | App-specific |

### Password Storage
```python
# ✅ GOOD: Environment variables
import os
password = os.environ.get('MAIL_PASSWORD')

# ❌ BAD: Hardcoded in code
password = "my-secret-password"

# ❌ BAD: In configuration files
password = "my-secret-password"  # config.py
```

---

## 📧 Email Security Configuration

### Gmail Setup (Recommended)
```env
# ✅ SECURE: Gmail with App Password
MAIL_PROVIDER=gmail
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-character-app-password
```

### Alternative Providers
```env
# Outlook Configuration
MAIL_PROVIDER=outlook
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=True

# Zoho Mail Configuration  
MAIL_PROVIDER=zoho
MAIL_SERVER=smtp.zoho.com
MAIL_PORT=587
MAIL_USE_TLS=True

# SendGrid (Production Recommended)
MAIL_PROVIDER=sendgrid
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key
```

---

## 🌐 Web Application Security

### Flask Security Settings
```python
# ✅ SECURE: Production configuration
class ProductionConfig(Config):
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SSL_STRICT = True
```

### HTTPS Configuration
```nginx
# ✅ GOOD: Nginx HTTPS configuration
server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/certificate.crt;
    ssl_certificate_key /path/to/private.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Security Headers
```python
# ✅ GOOD: Security headers middleware
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

---

## 🔍 Input Validation & Sanitization

### User Input Validation
```python
# ✅ GOOD: Validate email format
import re
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# ✅ GOOD: Sanitize user input
from werkzeug.utils import secure_filename
def sanitize_filename(filename):
    return secure_filename(filename)

# ✅ GOOD: Validate phone numbers
def validate_phone(phone):
    # Remove all non-digit characters
    digits = re.sub(r'\D', '', phone)
    return len(digits) >= 10 and len(digits) <= 15
```

### Database Security
```python
# ✅ GOOD: Use parameterized queries
from sqlalchemy import text
result = db.session.execute(text("SELECT * FROM users WHERE email = :email"), 
                          {'email': user_email})

# ❌ BAD: String concatenation (SQL injection risk)
# result = db.session.execute(f"SELECT * FROM users WHERE email = '{user_email}'")
```

---

## 🚨 Error Handling & Logging

### Secure Error Handling
```python
# ✅ GOOD: Don't expose sensitive information in errors
@app.errorhandler(Exception)
def handle_error(error):
    logger.error(f"Application error: {error}")
    return render_template('error.html'), 500

# ❌ BAD: Expose stack traces to users
# return f"Error: {error}", 500
```

### Secure Logging
```python
# ✅ GOOD: Log without sensitive data
logger.info(f"Email sent to {to_email}")
logger.error(f"Authentication failed for user {username}")

# ❌ BAD: Log passwords or sensitive data
# logger.info(f"Login attempt: {username}, {password}")
```

---

## 🔑 Access Control & Authentication

### Password Hashing
```python
# ✅ GOOD: Use strong password hashing
from werkzeug.security import generate_password_hash, check_password_hash

hashed_password = generate_password_hash(user_password, method='pbkdf2:sha256')
is_valid = check_password_hash(hashed_password, provided_password)
```

### Session Security
```python
# ✅ GOOD: Secure session configuration
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=24)

# ✅ GOOD: Session timeout check
@app.before_request
def check_session_timeout():
    if 'user_id' in session:
        last_activity = session.get('last_activity')
        if last_activity and time.time() - last_activity > 3600:  # 1 hour
            session.clear()
            return redirect(url_for('login'))
        session['last_activity'] = time.time()
```

---

## 📊 Monitoring & Auditing

### Security Monitoring
```python
# ✅ GOOD: Log security events
def log_security_event(event_type, details):
    logger.warning(f"SECURITY: {event_type} - {details}")

# Usage examples:
log_security_event("LOGIN_FAILED", f"IP: {request.remote_addr}, Email: {email}")
log_security_event("PASSWORD_RESET", f"Email: {email}")
log_security_event("ADMIN_ACCESS", f"User: {current_user.email}, IP: {request.remote_addr}")
```

### Rate Limiting
```python
# ✅ GOOD: Implement rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # Login logic
```

---

## 🗄️ Database Security

### Database Credentials
```env
# ✅ GOOD: Use environment variables
DATABASE_URL=postgresql://username:password@localhost/shopserv

# ❌ BAD: Hardcoded in application
# db_uri = "postgresql://username:password@localhost/shopserv"
```

### Database Security Best Practices
- ✅ Use least privilege principle for database users
- ✅ Enable database connection encryption
- ✅ Regular database backups with encryption
- ✅ Database activity monitoring
- ✅ Keep database software updated

---

## 🔄 Regular Security Tasks

### Daily/Weekly Tasks
- [ ] Review application logs for security events
- [ ] Check for failed login attempts
- [ ] Monitor unusual account activity
- [ ] Verify SSL certificate validity

### Monthly Tasks
- [ ] Update all dependencies
- [ ] Review and rotate API keys
- [ ] Audit user permissions
- [ ] Test backup restoration

### Quarterly Tasks
- [ ] Security audit of codebase
- [ ] Penetration testing
- [ ] Review and update security policies
- [ ] Employee security training

---

## 🚨 Incident Response

### Security Incident Checklist
1. **Identify** the scope and impact
2. **Contain** the immediate threat
3. **Assess** damage and data exposure
4. **Notify** affected parties
5. **Remediate** vulnerabilities
6. **Document** lessons learned
7. **Prevent** future occurrences

### Emergency Contacts
- **Security Team**: security@yourcompany.com
- **Legal Counsel**: legal@yourcompany.com
- **PR Team**: pr@yourcompany.com
- **IT Support**: support@yourcompany.com

---

## 📚 Security Resources

### Documentation
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/2.3.x/security/)
- [Gmail Security Guide](https://support.google.com/accounts/answer/6010255)

### Tools
- **Security Scanning**: `bandit`, `safety`
- **Dependency Checks**: `pip-audit`, `npm audit`
- **SSL Testing**: `sslscan`, `testssl.sh`
- **Penetration Testing**: `OWASP ZAP`, `Burp Suite`

### Training
- **Security Awareness Training**: Monthly
- **Code Security Review**: Quarterly
- **Incident Response Drills**: Bi-annually

---

## ✅ Security Checklist

### Pre-Deployment Checklist
- [ ] All passwords in environment variables
- [ ] No hardcoded credentials in code
- [ ] HTTPS enabled in production
- [ ] Security headers configured
- [ ] Input validation implemented
- [ ] Error handling secure
- [ ] Logging configured (no sensitive data)
- [ ] Rate limiting enabled
- [ ] CSRF protection enabled
- [ ] Session security configured
- [ ] Database connections encrypted
- [ ] Backups tested and verified

### Ongoing Security Checklist
- [ ] Dependencies updated regularly
- [ ] Security patches applied promptly
- [ ] Access reviews performed
- [ ] Security monitoring active
- [ ] Incident response plan tested
- [ ] Security training current

---

**🛡️ Remember**: Security is an ongoing process, not a one-time setup. Stay vigilant, keep learning, and prioritize security in every decision you make.

**📞 If you suspect a security breach**: Immediately contact your security team and follow your incident response procedures.
