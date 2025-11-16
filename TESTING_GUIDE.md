# 🧪 SHOP&SERV - Testing Guide

## 📋 Overview

This guide provides comprehensive testing instructions for all features of SHOP&SERV.

---

## 🚀 Pre-Testing Setup

### 1. Ensure Application is Running

```bash
python app.py
```

Visit: http://localhost:5000

### 2. Prepare Test Data

- **Test Email:** Use a real email you can access
- **Test Card:** 4242 4242 4242 4242 (Stripe test card)
- **Test Images:** Prepare some product images (JPG/PNG)

---

## 🧪 Test Scenarios

## 1. Authentication Testing

### Test 1.1: Customer Registration

**Steps:**
1. Go to http://localhost:5000
2. Click "Register"
3. Fill in form:
   - Full Name: Test Customer
   - Email: customer@test.com
   - Phone: 1234567890
   - Role: Customer
   - Password: test123
   - Confirm Password: test123
4. Click "Register"

**Expected Result:**
- ✅ Success message appears
- ✅ Redirected to login page
- ✅ User created in database

### Test 1.2: Shop Owner Registration

**Steps:**
1. Click "Register"
2. Fill in form:
   - Full Name: Test Shop Owner
   - Email: shopowner@test.com
   - Phone: 1234567890
   - Role: Shop Owner
   - Password: test123
   - Confirm Password: test123
3. Click "Register"

**Expected Result:**
- ✅ Success message
- ✅ Redirected to login
- ✅ Shop owner account created

### Test 1.3: Login

**Steps:**
1. Click "Login"
2. Enter credentials:
   - Email: customer@test.com
   - Password: test123
3. Click "Login"

**Expected Result:**
- ✅ Logged in successfully
- ✅ Redirected to dashboard
- ✅ User name appears in navbar

### Test 1.4: Forgot Password Flow

**Steps:**
1. Click "Login"
2. Click "Forgot Password?"
3. Enter email: customer@test.com
4. Click "Send OTP"
5. Check email for OTP code
6. Enter OTP code
7. Click "Verify OTP"
8. Enter new password
9. Click "Reset Password"

**Expected Result:**
- ✅ OTP email received
- ✅ OTP verified successfully
- ✅ Password reset successful
- ✅ Can login with new password

### Test 1.5: Logout

**Steps:**
1. Click on user name in navbar
2. Click "Logout"

**Expected Result:**
- ✅ Logged out successfully
- ✅ Redirected to homepage
- ✅ Login/Register buttons visible

---

## 2. Customer Features Testing

### Test 2.1: Browse Products

**Steps:**
1. Login as customer
2. Click "Products" in navbar
3. View product list

**Expected Result:**
- ✅ Products displayed in grid
- ✅ Product images shown
- ✅ Prices visible
- ✅ Stock information shown

### Test 2.2: Search Products

**Steps:**
1. Go to Products page
2. Enter search term in search box
3. Click "Filter"

**Expected Result:**
- ✅ Filtered products shown
- ✅ Only matching products displayed
- ✅ Search term retained

### Test 2.3: Filter by Category

**Steps:**
1. Go to Products page
2. Select category from dropdown
3. Click "Filter"

**Expected Result:**
- ✅ Products filtered by category
- ✅ Only selected category shown

### Test 2.4: View Product Detail

**Steps:**
1. Click on any product
2. View product detail page

**Expected Result:**
- ✅ Product image displayed
- ✅ Full description shown
- ✅ Price and stock visible
- ✅ Shop name displayed
- ✅ "Add to Cart" button present

### Test 2.5: Add to Cart

**Steps:**
1. On product detail page
2. Click "Add to Cart"

**Expected Result:**
- ✅ Success message appears
- ✅ Cart badge updates
- ✅ Item added to cart

### Test 2.6: View Cart

**Steps:**
1. Click "Cart" in navbar
2. View cart items

**Expected Result:**
- ✅ All cart items displayed
- ✅ Quantities shown
- ✅ Prices calculated
- ✅ Total amount shown

### Test 2.7: Update Cart Quantity

**Steps:**
1. In cart, change quantity
2. Quantity updates automatically

**Expected Result:**
- ✅ Quantity updated
- ✅ Price recalculated
- ✅ Total updated

### Test 2.8: Remove from Cart

**Steps:**
1. In cart, click "Remove"
2. Confirm removal

**Expected Result:**
- ✅ Item removed
- ✅ Cart updated
- ✅ Total recalculated

### Test 2.9: Checkout

**Steps:**
1. In cart, click "Proceed to Checkout"
2. Fill in shipping information:
   - Address: 123 Test Street, Test City
   - Phone: 1234567890
   - Notes: Test order
3. Click "Continue to Payment"

**Expected Result:**
- ✅ Redirected to payment page
- ✅ Order created
- ✅ Order summary shown

### Test 2.10: Payment

**Steps:**
1. On payment page
2. Enter card details:
   - Card: 4242 4242 4242 4242
   - Expiry: Any future date (e.g., 12/25)
   - CVC: Any 3 digits (e.g., 123)
3. Click "Pay"

**Expected Result:**
- ✅ Payment processing shown
- ✅ Payment successful
- ✅ Redirected to success page
- ✅ Order confirmed
- ✅ Cart cleared

### Test 2.11: View Order History

**Steps:**
1. Go to Dashboard
2. View order list

**Expected Result:**
- ✅ All orders displayed
- ✅ Order numbers shown
- ✅ Status visible
- ✅ Payment status shown

### Test 2.12: View Order Details

**Steps:**
1. In order history
2. Click "View Details"

**Expected Result:**
- ✅ Order details shown
- ✅ Items listed
- ✅ Shipping info displayed
- ✅ Total amount shown

### Test 2.13: Update Profile

**Steps:**
1. Click user name → "Profile"
2. Update information
3. Click "Update Profile"

**Expected Result:**
- ✅ Profile updated
- ✅ Success message shown
- ✅ Changes saved

---

## 3. Shop Owner Features Testing

### Test 3.1: Create Shop

**Steps:**
1. Login as shop owner
2. Click "Create Shop"
3. Fill in form:
   - Name: Test Shop
   - Description: A test shop
   - Address: 123 Shop Street
   - Upload logo (optional)
4. Click "Create Shop"

**Expected Result:**
- ✅ Shop created
- ✅ Redirected to dashboard
- ✅ Shop information displayed

### Test 3.2: Edit Shop

**Steps:**
1. Go to Shop Dashboard
2. Click "Edit Shop"
3. Modify information
4. Click "Update Shop"

**Expected Result:**
- ✅ Shop updated
- ✅ Changes saved
- ✅ Success message shown

### Test 3.3: Add Product

**Steps:**
1. Go to "My Products"
2. Click "Add New Product"
3. Fill in form:
   - Name: Test Product
   - Description: A test product
   - Price: 99.99
   - Stock: 50
   - Category: Electronics
   - Upload image
4. Click "Add Product"

**Expected Result:**
- ✅ Product created
- ✅ Image uploaded
- ✅ Product appears in list

### Test 3.4: Edit Product

**Steps:**
1. In product list
2. Click "Edit" on a product
3. Modify details
4. Click "Update Product"

**Expected Result:**
- ✅ Product updated
- ✅ Changes saved
- ✅ Success message shown

### Test 3.5: Delete Product

**Steps:**
1. In product list
2. Click "Delete"
3. Confirm deletion

**Expected Result:**
- ✅ Product deleted
- ✅ Removed from list
- ✅ Success message shown

### Test 3.6: View Orders

**Steps:**
1. After customer places order
2. Go to "Orders"
3. View order list

**Expected Result:**
- ✅ Orders displayed
- ✅ Customer info shown
- ✅ Product details visible
- ✅ Status shown

### Test 3.7: Update Order Status

**Steps:**
1. In orders list
2. Select new status from dropdown
3. Status updates

**Expected Result:**
- ✅ Status updated
- ✅ Customer notified
- ✅ Success message shown

### Test 3.8: View Dashboard Analytics

**Steps:**
1. Go to Shop Dashboard
2. View statistics

**Expected Result:**
- ✅ Total products shown
- ✅ Total orders shown
- ✅ Revenue displayed
- ✅ Recent orders listed

---

## 4. Admin Features Testing

### Test 4.1: Admin Login

**Steps:**
1. Logout if logged in
2. Login with:
   - Email: admin@shopserv.com
   - Password: admin123

**Expected Result:**
- ✅ Logged in as admin
- ✅ Admin dashboard visible

### Test 4.2: View Dashboard

**Steps:**
1. View admin dashboard
2. Check statistics

**Expected Result:**
- ✅ Total users shown
- ✅ Total shops shown
- ✅ Total products shown
- ✅ Total orders shown
- ✅ Revenue displayed

### Test 4.3: Manage Users

**Steps:**
1. Click "Manage Users"
2. View user list

**Expected Result:**
- ✅ All users displayed
- ✅ Roles shown
- ✅ Status visible
- ✅ Actions available

### Test 4.4: Disable/Enable User

**Steps:**
1. In user list
2. Click "Disable" on a user
3. Click "Enable" to re-enable

**Expected Result:**
- ✅ User disabled
- ✅ User cannot login when disabled
- ✅ User can login when enabled

### Test 4.5: Manage Shops

**Steps:**
1. Click "Manage Shops"
2. View shop list

**Expected Result:**
- ✅ All shops displayed
- ✅ Owner info shown
- ✅ Status visible

### Test 4.6: Disable/Enable Shop

**Steps:**
1. In shop list
2. Click "Disable" on a shop
3. Shop owner receives notification

**Expected Result:**
- ✅ Shop disabled
- ✅ Products hidden from customers
- ✅ Owner notified

### Test 4.7: Manage Products

**Steps:**
1. Click "Manage Products"
2. View all products

**Expected Result:**
- ✅ All products listed
- ✅ Shop names shown
- ✅ Status visible

### Test 4.8: Disable/Enable Product

**Steps:**
1. In product list
2. Click "Disable" on a product

**Expected Result:**
- ✅ Product disabled
- ✅ Hidden from customers
- ✅ Still visible to shop owner

### Test 4.9: View All Orders

**Steps:**
1. Click "Manage Orders"
2. View order list

**Expected Result:**
- ✅ All orders displayed
- ✅ Customer info shown
- ✅ Payment status visible
- ✅ Order status shown

---

## 5. Notification Testing

### Test 5.1: Receive Notifications

**Steps:**
1. Perform actions that trigger notifications:
   - Place order (shop owner notified)
   - Update order status (customer notified)
   - Disable shop (owner notified)

**Expected Result:**
- ✅ Notification badge appears
- ✅ Count updates
- ✅ Notification icon shows badge

### Test 5.2: View Notifications

**Steps:**
1. Click notification icon
2. View notification dropdown

**Expected Result:**
- ✅ Notifications listed
- ✅ Recent notifications shown
- ✅ Timestamps visible

### Test 5.3: Mark as Read

**Steps:**
1. Click on a notification

**Expected Result:**
- ✅ Notification marked as read
- ✅ Badge count decreases
- ✅ Notification removed from list

---

## 6. Security Testing

### Test 6.1: Unauthorized Access

**Steps:**
1. Logout
2. Try to access:
   - /dashboard
   - /shop/dashboard
   - /admin/dashboard

**Expected Result:**
- ✅ Redirected to login
- ✅ Access denied message

### Test 6.2: Role-based Access

**Steps:**
1. Login as customer
2. Try to access /shop/dashboard
3. Try to access /admin/dashboard

**Expected Result:**
- ✅ Access denied
- ✅ Redirected appropriately

### Test 6.3: CSRF Protection

**Steps:**
1. Inspect form
2. Check for CSRF token

**Expected Result:**
- ✅ CSRF token present
- ✅ Form submission requires token

### Test 6.4: Password Security

**Steps:**
1. Try to register with weak password (< 6 chars)

**Expected Result:**
- ✅ Error message shown
- ✅ Registration prevented

### Test 6.5: File Upload Security

**Steps:**
1. Try to upload non-image file as product image

**Expected Result:**
- ✅ Upload rejected
- ✅ Error message shown

---

## 7. UI/UX Testing

### Test 7.1: Responsive Design

**Steps:**
1. Resize browser window
2. Test on mobile size
3. Test on tablet size

**Expected Result:**
- ✅ Layout adjusts
- ✅ Navigation works
- ✅ All features accessible

### Test 7.2: Animations

**Steps:**
1. Navigate through pages
2. Observe transitions

**Expected Result:**
- ✅ Smooth animations
- ✅ Fade-in effects work
- ✅ Hover effects present

### Test 7.3: Flash Messages

**Steps:**
1. Perform any action
2. Observe flash messages

**Expected Result:**
- ✅ Messages appear
- ✅ Auto-dismiss after 5 seconds
- ✅ Can be manually closed

### Test 7.4: Form Validation

**Steps:**
1. Submit empty form
2. Submit invalid data

**Expected Result:**
- ✅ Validation errors shown
- ✅ Fields highlighted
- ✅ Helpful error messages

---

## 8. Performance Testing

### Test 8.1: Page Load Time

**Steps:**
1. Open browser dev tools
2. Navigate to pages
3. Check load times

**Expected Result:**
- ✅ Pages load quickly
- ✅ Images optimized
- ✅ No significant delays

### Test 8.2: Image Upload

**Steps:**
1. Upload large image (< 16MB)
2. Check processing

**Expected Result:**
- ✅ Image uploaded
- ✅ Image optimized
- ✅ Thumbnail created

---

## 9. Error Handling Testing

### Test 9.1: 404 Error

**Steps:**
1. Visit non-existent URL
2. Example: /nonexistent

**Expected Result:**
- ✅ Custom 404 page shown
- ✅ "Go Home" button present

### Test 9.2: Invalid Product ID

**Steps:**
1. Visit /product/99999

**Expected Result:**
- ✅ 404 error shown
- ✅ Graceful handling

### Test 9.3: Database Error

**Steps:**
1. Delete database file
2. Restart application

**Expected Result:**
- ✅ Database recreated
- ✅ Admin user created
- ✅ Application works

---

## 📊 Test Results Template

Use this template to record test results:

```
Test ID: [e.g., 1.1]
Test Name: [e.g., Customer Registration]
Date: [Date tested]
Tester: [Your name]
Status: [Pass/Fail]
Notes: [Any observations]
```

---

## ✅ Testing Checklist

- [ ] All authentication tests passed
- [ ] All customer features tested
- [ ] All shop owner features tested
- [ ] All admin features tested
- [ ] Notifications working
- [ ] Security measures verified
- [ ] UI/UX responsive
- [ ] Performance acceptable
- [ ] Error handling works
- [ ] Payment integration tested

---

## 🐛 Bug Reporting

If you find bugs:

1. **Note the steps to reproduce**
2. **Record expected vs actual behavior**
3. **Check browser console for errors**
4. **Check Flask logs**
5. **Document environment details**

---

## 🎯 Test Coverage

This testing guide covers:
- ✅ 50+ test scenarios
- ✅ All user roles
- ✅ All major features
- ✅ Security aspects
- ✅ UI/UX elements
- ✅ Error handling

---

**Happy Testing! 🧪**
