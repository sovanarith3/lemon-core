from flask import Flask, jsonify, request
import schedule
import time
import threading
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)

# Connect to PostgreSQL using DATABASE_URL from Railway
conn = psycopg2.connect(os.environ['DATABASE_URL'], cursor_factory=RealDictCursor)
cur = conn.cursor()

# Create thoughts table if not exists
cur.execute("""
    CREATE TABLE IF NOT EXISTS thoughts (
        id SERIAL PRIMARY KEY,
        content TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")
conn.commit()

# Explore function: generates a new thought
def explore():
    thought = "I just explored my environment at: " + time.ctime()
    print(thought)

    # Check if this thought already exists
    cur.execute("SELECT content FROM thoughts ORDER BY id DESC LIMIT 1;")
    last = cur.fetchone()
    if not last or last["content"] != thought:
        cur.execute("INSERT INTO thoughts (content) VALUES (%s);", (thought,))
        conn.commit()

    # Delete old ones if more than 50 exist
    cur.execute("DELETE FROM thoughts WHERE id NOT IN (SELECT id FROM thoughts ORDER BY timestamp DESC LIMIT 50);")
    conn.commit()

# View all stored thoughts
@app.route('/api/memory', methods=['GET'])
def get_memory():
    cur.execute("SELECT * FROM thoughts ORDER BY timestamp DESC;")
    rows = cur.fetchall()
    return jsonify(rows)

# Home route
@app.route('/')
def home():
    return "Indra is online with smart memory."

# Background scheduling
schedule.every(1).minutes.do(explore)
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_schedule, daemon=True).start()
