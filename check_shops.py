#!/usr/bin/env python3
"""
Simple script to check and update shop contact information
"""

import sqlite3
import os
from datetime import datetime

def update_shop_contacts():
    """Update shop contact information directly in SQLite database"""
    
    db_path = os.path.join(os.getcwd(), 'instance', 'shopserv.db')
    
    if not os.path.exists(db_path):
        print("❌ Database not found. Please run the application first to create the database.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if shops table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='shops'")
        if not cursor.fetchone():
            print("❌ Shops table not found in database.")
            return
        
        # Get all shops
        cursor.execute("SELECT id, name, contact_phone, contact_whatsapp, contact_email, opening_time, closing_time FROM shops")
        shops = cursor.fetchall()
        
        if not shops:
            print("❌ No shops found in database.")
            return
        
        print(f"📋 Found {len(shops)} shops in database")
        print("-" * 60)
        
        updated_count = 0
        
        for shop in shops:
            shop_id, name, phone, whatsapp, email, opening_time, closing_time = shop
            needs_update = False
            updates = []
            
            # Check and update missing fields
            if not phone:
                phone = "0000000000"
                updates.append(("contact_phone", phone))
                needs_update = True
                print(f"📱 Added phone for {name}: {phone}")
            
            if not whatsapp and phone:
                whatsapp = phone
                updates.append(("contact_whatsapp", whatsapp))
                needs_update = True
                print(f"💬 Added WhatsApp for {name}: {whatsapp}")
            
            if not opening_time:
                opening_time = "09:00:00"
                updates.append(("opening_time", opening_time))
                needs_update = True
                print(f"🕐 Added opening time for {name}: 09:00")
            
            if not closing_time:
                closing_time = "18:00:00"
                updates.append(("closing_time", closing_time))
                needs_update = True
                print(f"🕐 Added closing time for {name}: 18:00")
            
            # Apply updates
            if needs_update and updates:
                set_clause = ", ".join([f"{field} = ?" for field, _ in updates])
                values = [value for _, value in updates] + [shop_id]
                cursor.execute(f"UPDATE shops SET {set_clause}, updated_at = ? WHERE id = ?", 
                             values + [datetime.utcnow().isoformat(), shop_id])
                updated_count += 1
        
        # Commit changes
        if updated_count > 0:
            conn.commit()
            print(f"\n✅ Successfully updated {updated_count} shops")
        else:
            print("✅ All shops already have contact information")
        
        # Display current shop info
        print("\n📋 Current Shop Contact Information:")
        print("-" * 60)
        cursor.execute("SELECT name, contact_phone, contact_whatsapp, contact_email, address, city, state, pincode, opening_time, closing_time FROM shops")
        for shop in cursor.fetchall():
            name, phone, whatsapp, email, address, city, state, pincode, opening_time, closing_time = shop
            print(f"🏪 {name}")
            print(f"   📱 Phone: {phone or 'Not set'}")
            print(f"   💬 WhatsApp: {whatsapp or 'Not set'}")
            print(f"   📧 Email: {email or 'Not set'}")
            addr_parts = [part for part in [address, city, state, pincode] if part]
            print(f"   📍 Address: {', '.join(addr_parts) if addr_parts else 'Not set'}")
            print(f"   🕐 Hours: {opening_time or 'Not set'} - {closing_time or 'Not set'}")
            print("-" * 60)
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    update_shop_contacts()
