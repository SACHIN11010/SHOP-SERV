"""Quick script to update email configuration"""

# Read .env file
with open('.env', 'r') as f:
    lines = f.readlines()

# Update email settings
new_lines = []
updated = {'username': False, 'password': False, 'sender': False}

for line in lines:
    if line.startswith('MAIL_USERNAME='):
        new_lines.append('MAIL_USERNAME=sachindarji2600@gmail.com\n')
        updated['username'] = True
    elif line.startswith('MAIL_PASSWORD='):
        new_lines.append('MAIL_PASSWORD=lnypalanymxnlafk\n')
        updated['password'] = True
    elif line.startswith('MAIL_DEFAULT_SENDER='):
        new_lines.append('MAIL_DEFAULT_SENDER=sachindarji2600@gmail.com\n')
        updated['sender'] = True
    else:
        new_lines.append(line)

# Add missing settings
if not updated['username']:
    new_lines.append('MAIL_USERNAME=sachindarji2600@gmail.com\n')
if not updated['password']:
    new_lines.append('MAIL_PASSWORD=lnypalanymxnlafk\n')
if not updated['sender']:
    new_lines.append('MAIL_DEFAULT_SENDER=sachindarji2600@gmail.com\n')

# Write back
with open('.env', 'w') as f:
    f.writelines(new_lines)

print("✅ Email configuration updated successfully!")
print("\n📧 Email: sachindarji2600@gmail.com")
print("🔑 Password: ****configured****")
print("\n✨ Your forgot password system is now ready!")
print("\n🚀 Next steps:")
print("1. Restart your Flask application")
print("2. Test the 'Forgot Password' feature")
print("3. OTP will be sent to registered email addresses")
