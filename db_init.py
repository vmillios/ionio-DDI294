import sqlite3
import os
import yaml

def load_config():
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    return config['app']

CONFIG = load_config()
DB_NAME = CONFIG['db_name']

def init_db():
    if os.path.exists(DB_NAME):
        return
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        age INTEGER
    )''')
    # Insert 30 rows of sample data
    for i in range(1, 31):
        name = f'Customer{i}'
        email = f'customer{i}@example.com'
        age = 20 + (i % 30)
        c.execute('INSERT INTO customers (name, email, age) VALUES (?, ?, ?)', (name, email, age))
    conn.commit()
    conn.close()
