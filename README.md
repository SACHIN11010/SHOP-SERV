# SHOP&SERV - E-Commerce Platform

A full-featured, production-ready e-commerce web application built with Flask, featuring role-based access control, payment integration, and modern UI/UX.

## 🚀 Features

### Customer Features
- User registration and authentication with secure password hashing
- Forgot password with OTP verification via email
- Browse and search products by name and category
- Add products to cart and manage quantities
- Secure checkout process
- Real payment integration with Stripe
- View order history and track order status
- Profile management

### Shop Owner Features
- Separate registration as shop owner
- Create and manage shop profile with logo
- Add, edit, and delete products with images
- Manage product inventory (stock, price, category)
- View and manage orders
- Update order status (confirmed, processing, shipped, delivered)
- Dashboard with sales analytics

### Admin Features
- Comprehensive admin dashboard
- Manage all users (customers and shop owners)
- Enable/disable user accounts
- Manage all shops and products
- View all orders and transactions
- Platform-wide analytics and statistics

### Security Features
- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- Session management with secure cookies
- Role-based access control
- Safe file upload handling with validation
- Input validation and sanitization

### Technical Features
- Modern, responsive UI with CSS animations
- Real-time notifications system
- Email integration for OTP and notifications
- Image optimization and thumbnail generation
- SQLite database with proper relationships
- RESTful API endpoints
- Production-ready code structure

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A Gmail account for sending emails (or other SMTP server)
- Stripe account for payment processing (test mode is fine)

## 🛠️ Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd D:\SHO&SERV
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     copy .env.example .env
     ```
   - Edit `.env` and fill in your credentials:
     - `SECRET_KEY`: Generate a random secret key
     - `STRIPE_PUBLIC_KEY`: Your Stripe publishable key
     - `STRIPE_SECRET_KEY`: Your Stripe secret key
     - `MAIL_USERNAME`: Your Gmail address
     - `MAIL_PASSWORD`: Your Gmail app password (not regular password)
     - `MAIL_DEFAULT_SENDER`: Your Gmail address

## 📧 Setting Up Gmail for Email

1. Go to your Google Account settings
2. Enable 2-Factor Authentication
3. Generate an App Password:
   - Go to Security > 2-Step Verification > App passwords
   - Select "Mail" and "Windows Computer"
   - Copy the generated 16-character password
   - Use this as `MAIL_PASSWORD` in your `.env` file

## 💳 Setting Up Stripe

1. Create a Stripe account at https://stripe.com
2. Go to Developers > API keys
3. Copy your Publishable key and Secret key
4. Add them to your `.env` file
5. Use test mode for development (test keys start with `pk_test_` and `sk_test_`)

## 🚀 Running the Application

1. **Start the Flask development server:**
   ```bash
   python app.py
   ```

2. **Access the application:**
   - Open your browser and go to: `http://localhost:5000`

3. **Default Admin Credentials:**
   - Email: `admin@shopserv.com`
   - Password: `admin123`
   - **⚠️ IMPORTANT: Change these credentials immediately after first login!**

## 📁 Project Structure

```
D:\SHO&SERV\
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── models.py              # Database models
├── forms.py               # WTForms definitions
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create from .env.example)
├── .env.example          # Example environment variables
├── README.md             # This file
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   ├── js/
│   │   └── main.js       # JavaScript functionality
│   └── uploads/          # User-uploaded images
│       ├── products/     # Product images
│       └── shops/        # Shop logos
└── templates/
    ├── base.html         # Base template
    ├── index.html        # Homepage
    ├── login.html        # Login page
    ├── register.html     # Registration page
    ├── products.html     # Products listing
    ├── cart.html         # Shopping cart
    ├── checkout.html     # Checkout page
    ├── payment.html      # Payment page
    ├── customer/         # Customer templates
    ├── shop/             # Shop owner templates
    ├── admin/            # Admin templates
    └── errors/           # Error pages
```

## 🎨 User Roles

### Customer
- Browse and purchase products
- Manage shopping cart
- Complete checkout with payment
- View order history

### Shop Owner
- Manage shop profile
- Add/edit/delete products
- View and fulfill orders
- Track sales and revenue

### Admin
- Full platform control
- User management
- Shop and product moderation
- System-wide analytics

## 🔒 Security Best Practices

1. **Change default admin password immediately**
2. **Use strong SECRET_KEY in production**
3. **Never commit `.env` file to version control**
4. **Use HTTPS in production**
5. **Keep dependencies updated**
6. **Use environment-specific configurations**

## 🌐 Deployment

### Deploying to Render/Heroku

1. **Update configuration for production:**
   - Set `SESSION_COOKIE_SECURE = True` in `config.py`
   - Use PostgreSQL instead of SQLite for production
   - Set proper environment variables on the hosting platform

2. **Create a `Procfile`:**
   ```
   web: gunicorn app:app
   ```

3. **Add gunicorn to requirements.txt:**
   ```bash
   pip install gunicorn
   pip freeze > requirements.txt
   ```

4. **Deploy to your chosen platform**

## 📝 Testing

### Test Payment Cards (Stripe Test Mode)

- **Success:** 4242 4242 4242 4242
- **Decline:** 4000 0000 0000 0002
- Use any future expiry date and any 3-digit CVC

### Test User Accounts

Create test accounts for each role:
1. Customer account for testing purchases
2. Shop owner account for testing shop management
3. Use admin account for platform management

## 🐛 Troubleshooting

### Database Issues
```bash
# Delete the database and recreate
rm shopserv.db
python app.py
```

### Email Not Sending
- Verify Gmail app password is correct
- Check that 2FA is enabled on Gmail
- Ensure SMTP settings are correct in `.env`

### Payment Issues
- Verify Stripe keys are correct
- Check that you're using test mode keys for development
- Ensure JavaScript is enabled in browser

## 📚 Technologies Used

- **Backend:** Flask, SQLAlchemy, Flask-Login, Flask-Mail
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Database:** SQLite (development), PostgreSQL (production recommended)
- **Payment:** Stripe API
- **Security:** Werkzeug, Flask-WTF, itsdangerous
- **Image Processing:** Pillow

## 🤝 Support

For issues or questions:
1. Check this README
2. Review error messages in the console
3. Check Flask logs
4. Verify environment variables are set correctly

## 📄 License

This project is created for educational purposes.

## 🎓 College Submission Notes

This is a complete, production-ready e-commerce platform suitable for:
- College projects and submissions
- Portfolio demonstrations
- Learning full-stack web development
- Understanding e-commerce workflows

**Key Highlights for Evaluation:**
- ✅ Complete CRUD operations
- ✅ Role-based access control
- ✅ Real payment integration
- ✅ Email/OTP authentication
- ✅ Modern, responsive UI
- ✅ Security best practices
- ✅ Production-ready code structure
- ✅ Comprehensive documentation

---

**Built with ❤️ for SHOP&SERV**
