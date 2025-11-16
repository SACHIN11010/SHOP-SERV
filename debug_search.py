import sqlite3

conn = sqlite3.connect('instance/shopserv.db')
cursor = conn.cursor()

# Check ZORO_FOOTWARE shop details
cursor.execute('SELECT name, city, service_type, is_active, is_approved FROM shops WHERE name LIKE ?', ('%ZORO%',))
for row in cursor.fetchall():
    print(f'Name: {row[0]}, City: {row[1]}, Type: {row[2]}, Active: {row[3]}, Approved: {row[4]}')

# Test search query with empty search
cursor.execute('SELECT name FROM shops WHERE is_active=1 AND is_approved=1')
print(f'\nActive shops: {[row[0] for row in cursor.fetchall()]}')

# Test with search term
cursor.execute('SELECT name FROM shops WHERE is_active=1 AND is_approved=1 AND name LIKE ?', ('%ZORO%',))
print(f'Search results for ZORO: {[row[0] for row in cursor.fetchall()]}')

conn.close()
