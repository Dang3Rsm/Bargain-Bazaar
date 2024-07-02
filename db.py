import sqlite3

conn = sqlite3.connect("BB.sqlite")
cur = conn.cursor()



# Create ads_master_table
sql_query = '''
    CREATE TABLE IF NOT EXISTS ads_master_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price NUMERIC(10, 2) NOT NULL,
    img_urls TEXT,
    tags TEXT,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    deletion_date TIMESTAMP,
    published BOOLEAN DEFAULT 0
);
'''
cur.execute(sql_query)

# Create tags table
sql_query = '''
    CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE
);
'''
cur.execute(sql_query)

# Create ad_tags junction table
sql_query = '''
    CREATE TABLE IF NOT EXISTS ad_tags (
    ad_id INTEGER,
    tag_id INTEGER,
    PRIMARY KEY (ad_id, tag_id),
    FOREIGN KEY (ad_id) REFERENCES ads_master_table(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);
'''
cur.execute(sql_query)

conn.commit()
conn.close()
