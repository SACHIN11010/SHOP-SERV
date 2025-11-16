#!/usr/bin/env python3
"""
Verify all shop fields are correct
"""

import sqlite3
import os

def verify_shop_data():
    """Verify all required shop fields"""
    
    db_path = os.path.join(os.getcwd(), 'instance', 'shopserv.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all shop data
        cursor.execute("""
            SELECT id, name, city, service_type, is_active, is_approved, 
                   contact_phone, created_at, updated_at
            FROM shops 
            WHERE name = 'ZORO_FOOTWARE'
        """)
        
        shop = cursor.fetchone()
        
        if shop:
            print(f"📋 Complete Shop Data:")
            print(f"   ID: {shop[0]}")
            print(f"   Name: {shop[1]}")
            print(f"   City: '{shop[2]}'")
            print(f"   Service Type: '{shop[3]}'")
            print(f"   Active: {shop[4]}")
            print(f"   Approved: {shop[5]}")
            print(f"   Phone: {shop[6]}")
            print(f"   Created: {shop[7]}")
            print(f"   Updated: {shop[8]}")
        else:
            print("❌ Shop not found")
        
        # Check all shops
        cursor.execute("SELECT COUNT(*) FROM shops WHERE is_active=1 AND is_approved=1")
        count = cursor.fetchone()[0]
        print(f"\n📊 Total active/approved shops: {count}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    verify_shop_data()
