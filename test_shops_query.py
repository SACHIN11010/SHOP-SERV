#!/usr/bin/env python3
"""
Test the shops query directly
"""

import sqlite3
import os

def test_shops_query():
    """Test the exact same query as the shops route"""
    
    db_path = os.path.join(os.getcwd(), 'instance', 'shopserv.db')
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Test base query (same as shops route)
        cursor.execute("""
            SELECT id, name, city, service_type, is_active, is_approved 
            FROM shops 
            WHERE is_active = 1 AND is_approved = 1
            ORDER BY created_at DESC
        """)
        
        shops = cursor.fetchall()
        
        print(f"📊 Found {len(shops)} active/approved shops:")
        for shop in shops:
            print(f"   - {shop[1]} (City: {shop[2]}, Type: {shop[3]})")
        
        # Test with search filter
        cursor.execute("""
            SELECT id, name, city, service_type, is_active, is_approved 
            FROM shops 
            WHERE is_active = 1 AND is_approved = 1
            AND name LIKE '%zor%'
            ORDER BY created_at DESC
        """)
        
        search_results = cursor.fetchall()
        print(f"\n🔍 Search 'zor' results: {len(search_results)} shops")
        
        # Test with city filter
        cursor.execute("""
            SELECT id, name, city, service_type, is_active, is_approved 
            FROM shops 
            WHERE is_active = 1 AND is_approved = 1
            AND city LIKE '%Patan%'
            ORDER BY created_at DESC
        """)
        
        city_results = cursor.fetchall()
        print(f"🏙️ City 'Patan' results: {len(city_results)} shops")
        
        # Test with service_type filter
        cursor.execute("""
            SELECT id, name, city, service_type, is_active, is_approved 
            FROM shops 
            WHERE is_active = 1 AND is_approved = 1
            AND service_type = 'Footwear'
            ORDER BY created_at DESC
        """)
        
        type_results = cursor.fetchall()
        print(f"👟 Type 'Footwear' results: {len(type_results)} shops")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    test_shops_query()
