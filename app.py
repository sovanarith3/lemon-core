# app.py
from flask import Flask, render_template
import psycopg2
import os

app = Flask(__name__)

# Database connection
database_url = os.getenv("DATABASE")
if not database_url:
raise ValueError("DATABASE environment variable not set")

try:
conn = psycopg2.connect(database_url)
cur = conn.cursor()
except Exception as e:
print(f"Database connection failed: {e}")
raise

@app.route('/')
def home():
cur.execute("SELECT action, outcome, timestamp FROM indra_memory ORDER BY timestamp DESC LIMIT 10")
logs = cur.fetchall()
return render_template('index.html', logs=logs)

@app.route('/stop_indra', methods=['POST'])
def stop_indra():
cur.execute("INSERT INTO indra_memory (action, outcome) VALUES (%s, %s)", ("Stopped Indra", "Manual shutdown"))
conn.commit()
os._exit(0)
return "Indra stopped"

if __name__ == "__main__":
app.run(host="0.0.0.0", port=8080)

# Cleanup
import atexit
@atexit.register
def cleanup():
if 'conn' in globals() and conn:
cur.close()
conn.close()
print("Database connection closed.")
