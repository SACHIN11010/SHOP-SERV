#!/usr/bin/env python3
"""
Check shop approval status
"""

import sqlite3
import os

def check_shop_status():
    """Check if shop is approved and active"""
    
    db_path = os.path.join(os.getcwd(), 'instance', 'shopserv.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check shop status
        cursor.execute("SELECT name, is_active, is_approved FROM shops WHERE name = 'ZORO_FOOTWARE'")
        shop = cursor.fetchone()
        
        if shop:
            print(f"📋 Shop Status for {shop[0]}:")
            print(f"   Active: {shop[1]}")
            print(f"   Approved: {shop[2]}")
            
            if not shop[1] or not shop[2]:
                print("❌ Shop needs to be active and approved to appear in shops listing")
                # Update to make it active and approved
                cursor.execute("""
                    UPDATE shops 
                    SET is_active = 1, 
                        is_approved = 1
                    WHERE name = 'ZORO_FOOTWARE'
                """)
                conn.commit()
                print("✅ Updated shop to be active and approved")
        else:
            print("❌ Shop not found")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    check_shop_status()
