"""
Verification script for SHOP&SERV
Checks if all required files and directories exist
"""
import os
import sys

def check_file(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ MISSING {description}: {filepath}")
        return False

def check_directory(dirpath, description):
    """Check if a directory exists"""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        print(f"✓ {description}: {dirpath}")
        return True
    else:
        print(f"✗ MISSING {description}: {dirpath}")
        return False

def main():
    print("=" * 60)
    print("SHOP&SERV - Setup Verification")
    print("=" * 60)
    print()
    
    all_good = True
    
    # Core files
    print("Checking Core Files:")
    all_good &= check_file("app.py", "Main application")
    all_good &= check_file("models.py", "Database models")
    all_good &= check_file("forms.py", "Form definitions")
    all_good &= check_file("config.py", "Configuration")
    all_good &= check_file("utils.py", "Utility functions")
    all_good &= check_file("requirements.txt", "Dependencies")
    all_good &= check_file(".env", "Environment variables")
    print()
    
    # Documentation
    print("Checking Documentation:")
    all_good &= check_file("README.md", "Main documentation")
    all_good &= check_file("QUICKSTART.md", "Quick start guide")
    all_good &= check_file("FEATURES.md", "Feature list")
    print()
    
    # Directories
    print("Checking Directories:")
    all_good &= check_directory("templates", "Templates directory")
    all_good &= check_directory("static", "Static files directory")
    all_good &= check_directory("static/css", "CSS directory")
    all_good &= check_directory("static/js", "JavaScript directory")
    all_good &= check_directory("static/uploads", "Uploads directory")
    print()
    
    # Templates
    print("Checking Templates:")
    all_good &= check_file("templates/base.html", "Base template")
    all_good &= check_file("templates/index.html", "Homepage")
    all_good &= check_file("templates/login.html", "Login page")
    all_good &= check_file("templates/register.html", "Register page")
    all_good &= check_file("templates/products.html", "Products page")
    all_good &= check_file("templates/cart.html", "Cart page")
    all_good &= check_file("templates/checkout.html", "Checkout page")
    all_good &= check_file("templates/payment.html", "Payment page")
    print()
    
    # Customer templates
    print("Checking Customer Templates:")
    all_good &= check_directory("templates/customer", "Customer directory")
    all_good &= check_file("templates/customer/dashboard.html", "Customer dashboard")
    all_good &= check_file("templates/customer/profile.html", "Customer profile")
    print()
    
    # Shop templates
    print("Checking Shop Owner Templates:")
    all_good &= check_directory("templates/shop", "Shop directory")
    all_good &= check_file("templates/shop/dashboard.html", "Shop dashboard")
    all_good &= check_file("templates/shop/create_shop.html", "Create shop")
    all_good &= check_file("templates/shop/products.html", "Shop products")
    all_good &= check_file("templates/shop/add_product.html", "Add product")
    all_good &= check_file("templates/shop/orders.html", "Shop orders")
    print()
    
    # Admin templates
    print("Checking Admin Templates:")
    all_good &= check_directory("templates/admin", "Admin directory")
    all_good &= check_file("templates/admin/dashboard.html", "Admin dashboard")
    all_good &= check_file("templates/admin/users.html", "Manage users")
    all_good &= check_file("templates/admin/shops.html", "Manage shops")
    all_good &= check_file("templates/admin/products.html", "Manage products")
    all_good &= check_file("templates/admin/orders.html", "Manage orders")
    print()
    
    # Static files
    print("Checking Static Files:")
    all_good &= check_file("static/css/style.css", "Main stylesheet")
    all_good &= check_file("static/js/main.js", "Main JavaScript")
    print()
    
    # Error pages
    print("Checking Error Pages:")
    all_good &= check_directory("templates/errors", "Errors directory")
    all_good &= check_file("templates/errors/404.html", "404 page")
    all_good &= check_file("templates/errors/403.html", "403 page")
    all_good &= check_file("templates/errors/500.html", "500 page")
    print()
    
    print("=" * 60)
    if all_good:
        print("✓ ALL CHECKS PASSED!")
        print("=" * 60)
        print()
        print("Next Steps:")
        print("1. Edit .env file with your credentials")
        print("2. Run: pip install -r requirements.txt")
        print("3. Run: python app.py")
        print("4. Visit: http://localhost:5000")
        print()
        print("Default Admin Login:")
        print("  Email: admin@shopserv.com")
        print("  Password: admin123")
        print()
        return 0
    else:
        print("✗ SOME FILES ARE MISSING!")
        print("=" * 60)
        print()
        print("Please ensure all files are present before running the application.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
