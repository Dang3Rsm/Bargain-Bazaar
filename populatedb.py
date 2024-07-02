import sqlite3

conn = sqlite3.connect("BB.sqlite")
cur = conn.cursor()


# Sample data for ads with image URLs
ads_data = [
    ("Bike for Sale", "A nice bike", 100.00, "bike, motorcycle", "https://images.unsplash.com/photo-1605459862899-f506150a7a80?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D")
]

# Insert sample ads into ads_master_table with image URLs
for ad in ads_data:
    sql_query = '''
        INSERT INTO ads_master_table (title, description, price, tags, img_urls)
        VALUES (?, ?, ?, ?, ?);
    '''
    cur.execute(sql_query, ad)

# Sample data for tags
tags_data = [
    ("bike"),
    ("motorcycle"),
    ("ipad"),
    ("Tablet"),
    ("new gen tablet"),
    ("iphone"),
    ("smartphone"),
    ("macbook"),
    ("ultrabook"),
    ("dslr"),
    ("digital camera")
]

# Insert sample tags into tags table
for tag in tags_data:
    sql_query = '''
        INSERT INTO tags (name)
        VALUES (?);
    '''
    cur.execute(sql_query, (tag,))

conn.commit()
conn.close()