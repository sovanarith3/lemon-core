from flask import Flask, render_template, send_file
import indra
import json
import os

app = Flask(__name__)
indra_instance = indra.IndraAI()  # Create instance for status/memory

@app.route('/')
def index():
    status = indra_instance.get_status()
    memory = indra_instance.get_memory()
    return render_template('index.html', status=status, memory=memory)

@app.route('/logs')
def logs():
    try:
        return send_file('/tmp/indra.log', as_attachment=True)
    except FileNotFoundError:
        return "Log file not found", 404

@app.route('/memory')
def memory():
    memory_data = indra_instance.get_memory()
    with open('/tmp/memory.json', 'w') as f:
        json.dump(memory_data, f)
    return send_file('/tmp/memory.json', as_attachment=True)

@app.route('/health')
def health():
    return {"status": "Flask is running", "worker_logs_exist": os.path.exists('/tmp/indra.log')}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
