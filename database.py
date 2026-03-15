#### `database.py` (資料庫邏輯)
```python
import sqlite3
import hashlib

def get_connection():
    conn = sqlite3.connect('health_app.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        nickname TEXT NOT NULL
    )''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS health_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        week INTEGER,
        weight REAL,
        height REAL,
        heart_rate INTEGER,
        mood TEXT,
        symptoms TEXT,
        sleep_quality TEXT,
        exercise TEXT,
        notes TEXT,
        sentiment TEXT,
        ai_advice TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )''')
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(email, password, nickname):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (email, password, nickname) VALUES (?, ?, ?)',
                       (email, hash_password(password), nickname))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?',
                   (email, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    return user

def add_health_log(user_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO health_logs (
        user_id, week, weight, height, heart_rate, mood, symptoms, 
        sleep_quality, exercise, notes, sentiment, ai_advice
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id, data.get('week'), data.get('weight'), data.get('height'), data.get('heart_rate'),
        data.get('mood'), data.get('symptoms'), data.get('sleep_quality'), data.get('exercise'),
        data.get('notes'), data.get('sentiment'), data.get('ai_advice')
    ))
    conn.commit()
    conn.close()

def get_user_logs(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM health_logs WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
    logs = cursor.fetchall()
    conn.close()
    return logs
