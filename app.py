from flask import Flask, render_template, send_file
import indra
import json

app = Flask(__name__)

@app.route('/')
def index():
    status = indra.get_status()
    try:
        with open('/tmp/memory.json', 'r') as f:
            memory = json.load(f)
    except FileNotFoundError:
        memory = []
    return render_template('index.html', status=status, memory=memory)

@app.route('/logs')
def logs():
    try:
        return send_file('/tmp/indra.log', as_attachment=True)
    except FileNotFoundError:
        return "Log file not found", 404

@app.route('/memory')
def memory():
    try:
        return send_file('/tmp/memory.json', as_attachment=True)
    except FileNotFoundError:
        return "Memory file not found", 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
