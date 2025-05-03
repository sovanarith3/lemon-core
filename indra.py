from flask import Flask, jsonify, request
import schedule
import time
import threading

app = Flask(__name__)

memory_log = []

# Home route
@app.route('/')
def home():
    return "Indra is online and exploring..."

# API to view memory log
@app.route('/api/memory', methods=['GET'])
def get_memory():
    return jsonify(memory_log)

# Indra's self-exploration logic
def explore():
    thought = "I just explored my environment at: " + time.ctime()
    print(thought)
    memory_log.append(thought)

# Schedule the self-exploration
schedule.every(1).minutes.do(explore)

# Background scheduler thread
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Start scheduler thread when Flask starts
threading.Thread(target=run_schedule, daemon=True).start()
