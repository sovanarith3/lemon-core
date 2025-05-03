from flask import Flask, jsonify, request
import schedule, threading, time
import psycopg2, os

app = Flask(__name__)
DATABASE_URL = os.getenv("DATABASE_URL")

# Initialize DB (create table if not exists)
def init_db():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS thoughts (
                    id SERIAL PRIMARY KEY,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        conn.commit()

init_db()

# Explore and save new thoughts
def explore():
    thought = "I just explored my environment at: " + time.ctime()
    print(thought)
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO thoughts (content) VALUES (%s)", (thought,))
            cur.execute("DELETE FROM thoughts WHERE id NOT IN (SELECT id FROM thoughts ORDER BY created_at DESC LIMIT 50)")
        conn.commit()

# Flask route to get latest thoughts
@app.route("/")
def home():
    return "Indra is online and exploring..."

@app.route("/api/memory", methods=["GET"])
def get_memory():
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT content, created_at FROM thoughts ORDER BY created_at DESC")
            rows = cur.fetchall()
    return jsonify([{"thought": row[0], "time": str(row[1])} for row in rows])

# Scheduler setup
schedule.every(1).minutes.do(explore)

def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=run_schedule, daemon=True).start()
