#!/usr/bin/env python3
"""
Update shop with missing city and service_type fields
"""

import sqlite3
import os
from datetime import datetime

def update_shop_fields():
    """Update shop with city and service_type"""
    
    db_path = os.path.join(os.getcwd(), 'instance', 'shopserv.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Update the shop with city and service_type
        cursor.execute("""
            UPDATE shops 
            SET city = 'Patan', 
                service_type = 'Footwear',
                updated_at = ?
            WHERE name = 'ZORO_FOOTWARE'
        """, (datetime.utcnow().isoformat(),))
        
        conn.commit()
        print("✅ Updated ZORO_FOOTWARE with city and service_type")
        
        # Verify the update
        cursor.execute("SELECT name, city, service_type FROM shops WHERE name = 'ZORO_FOOTWARE'")
        shop = cursor.fetchone()
        if shop:
            print(f"📋 Shop Info: {shop[0]}, City: {shop[1]}, Type: {shop[2]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    update_shop_fields()
