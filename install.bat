@echo off
echo ========================================
echo    SHOP^&SERV - Installation Script
echo ========================================
echo.
echo This script will:
echo 1. Install all required dependencies
echo 2. Set up environment configuration
echo 3. Prepare the application for first run
echo.
pause
echo.

echo [Step 1/3] Installing dependencies...
echo ========================================
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Please ensure Python and pip are installed correctly
    pause
    exit /b 1
)
echo.
echo Dependencies installed successfully!
echo.

echo [Step 2/3] Setting up environment...
echo ========================================
if not exist .env (
    copy .env.example .env
    echo .env file created from template
    echo.
    echo IMPORTANT: Please edit .env file and add your credentials:
    echo - Email settings for OTP functionality
    echo - Stripe API keys for payment processing
    echo - Secret key for security
    echo.
) else (
    echo .env file already exists
)
echo.

echo [Step 3/3] Creating upload directories...
echo ========================================
if not exist "static\uploads" mkdir "static\uploads"
if not exist "static\uploads\products" mkdir "static\uploads\products"
if not exist "static\uploads\shops" mkdir "static\uploads\shops"
if not exist "static\uploads\services" mkdir "static\uploads\services"
echo Upload directories created!
echo.

echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file with your credentials
echo 2. Run: python app.py
echo 3. Open: http://localhost:5000
echo.
echo Default admin login:
echo   Email: admin@shopserv.com
echo   Password: admin123
echo.
echo Or use static admin:
echo   Username: admin
echo   Password: ADMIN123
echo.
echo For detailed instructions, see:
echo - README.md
echo - QUICK_START.md
echo - SETUP_GUIDE.md
echo.
pause
