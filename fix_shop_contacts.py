#!/usr/bin/env python3
"""
Migration script to ensure all shops have proper contact information
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the app.py file as a module
import importlib.util
spec = importlib.util.spec_from_file_location("app_module", os.path.join(os.getcwd(), "app.py"))
app_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(app_module)

# Now we can access app and db
from models import Shop, User
from datetime import datetime

def migrate_shop_contact_info():
    """Add missing contact information to shops"""
    
    app = app_module.app
    db = app_module.db
    
    with app.app_context():
        shops = Shop.query.all()
        updated_count = 0
        
        for shop in shops:
            needs_update = False
            
            # Add default contact email if missing
            if not shop.contact_email and shop.owner:
                shop.contact_email = shop.owner.email
                needs_update = True
                print(f"Added contact email for {shop.name}: {shop.owner.email}")
            
            # Add default phone if missing
            if not shop.contact_phone:
                shop.contact_phone = "0000000000"  # Placeholder
                needs_update = True
                print(f"Added placeholder phone for {shop.name}")
            
            # Add default WhatsApp if missing
            if not shop.contact_whatsapp and shop.contact_phone:
                shop.contact_whatsapp = shop.contact_phone
                needs_update = True
                print(f"Added WhatsApp for {shop.name}: {shop.contact_phone}")
            
            # Add default hours if missing
            if not shop.opening_time:
                shop.opening_time = datetime.strptime("09:00", "%H:%M").time()
                needs_update = True
                print(f"Added opening time for {shop.name}: 09:00")
            
            if not shop.closing_time:
                shop.closing_time = datetime.strptime("18:00", "%H:%M").time()
                needs_update = True
                print(f"Added closing time for {shop.name}: 18:00")
            
            if needs_update:
                shop.updated_at = datetime.utcnow()
                updated_count += 1
        
        if updated_count > 0:
            try:
                db.session.commit()
                print(f"\n✅ Successfully updated {updated_count} shops with contact information")
            except Exception as e:
                db.session.rollback()
                print(f"\n❌ Error updating shops: {str(e)}")
        else:
            print("✅ All shops already have contact information")
        
        # Display current shop contact info
        print("\n📋 Current Shop Contact Information:")
        print("-" * 60)
        for shop in shops:
            print(f"🏪 {shop.name}")
            print(f"   📧 Email: {shop.contact_email or 'Not set'}")
            print(f"   📱 Phone: {shop.contact_phone or 'Not set'}")
            print(f"   💬 WhatsApp: {shop.contact_whatsapp or 'Not set'}")
            print(f"   📍 Address: {shop.address or 'Not set'}")
            print(f"   🕐 Hours: {shop.opening_time or 'Not set'} - {shop.closing_time or 'Not set'}")
            print("-" * 60)

if __name__ == "__main__":
    migrate_shop_contact_info()
