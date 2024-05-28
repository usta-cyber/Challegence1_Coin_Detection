import sqlite3
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS images (id TEXT PRIMARY KEY, filename TEXT, filepath TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS circles (image_id TEXT, circle_id INTEGER, bounding_box TEXT, centroid TEXT, radius REAL)''')
    conn.commit()
    conn.close()
def insert_image(image_id, filename, filepath):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO images (id, filename, filepath) VALUES (?, ?, ?)', (image_id, filename, filepath))
    conn.commit()
    conn.close()

def insert_circle(image_id, bounding_box, centroid, radius):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    circle_id = c.execute('SELECT COUNT(*) FROM circles WHERE image_id = ?', (image_id,)).fetchone()[0]
    c.execute('INSERT INTO circles (image_id, circle_id, bounding_box, centroid, radius) VALUES (?, ?, ?, ?, ?)', 
              (image_id, circle_id, str(bounding_box), str(centroid), radius))
    conn.commit()
    conn.close()

def get_circles(image_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM circles WHERE image_id = ?', (image_id,))
    circles = [{'circle_id': row[1], 'bounding_box': row[2], 'centroid': row[3], 'radius': row[4]} for row in c.fetchall()]
    conn.close()
    return circles

def get_circle(image_id, circle_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM circles WHERE image_id = ? AND circle_id = ?', (image_id, circle_id))
    row = c.fetchone()
    if row:
        circle = {'circle_id': row[1], 'bounding_box': row[2], 'centroid': row[3], 'radius': row[4]}
        conn.close()
        return circle
    conn.close()
    return None
