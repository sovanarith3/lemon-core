from flask import Flask, render_template, send_file
import indra
import json
import os
import logging

logging.basicConfig(level=logging.DEBUG)
logging.debug("Starting app.py")

app = Flask(__name__)
app.config['DEBUG'] = True
logging.debug("Flask app initialized")

# Log templates directory contents
templates_dir = os.path.join(app.root_path, 'templates')
logging.debug(f"Templates directory: {templates_dir}")
if os.path.exists(templates_dir):
    logging.debug(f"Templates directory contents: {os.listdir(templates_dir)}")
else:
    logging.error("Templates directory does not exist")

try:
    indra_instance = indra.IndraAI()
    logging.debug("IndraAI instance created for Flask")
except Exception as e:
    logging.error(f"Failed to create IndraAI instance: {str(e)}")
    raise

@app.route('/')
def index():
    try:
        status = indra_instance.get_status()
        memory = indra_instance.get_memory()
        logging.debug(f"Rendering index with status: {status}, memory: {memory}")
        try:
            return render_template('index.html', status=status, memory=memory)
        except Exception as e:
            logging.error(f"Template rendering failed: {str(e)}")
            raise
    except Exception as e:
        logging.error(f"Error in index route: {str(e)}")
        raise

@app.route('/logs')
def logs():
    try:
        logging.debug("Attempting to serve indra.log")
        return send_file('/tmp/indra.log', as_attachment=True)
    except FileNotFoundError:
        logging.error("Log file not found")
        return "Log file not found", 404

@app.route('/memory')
def memory():
    try:
        logging.debug("Attempting to serve memory.json")
        memory_data = indra_instance.get_memory()
        with open('/tmp/memory.json', 'w') as f:
            json.dump(memory_data, f)
        return send_file('/tmp/memory.json', as_attachment=True)
    except Exception as e:
        logging.error(f"Error serving memory: {str(e)}")
        return "Memory file not found", 404

@app.route('/health')
def health():
    logging.debug("Health check requested")
    return {
        "status": "Flask is running",
        "worker_logs_exist": os.path.exists('/tmp/indra.log'),
        "memory_file_exists": os.path.exists('/tmp/memory.json')
    }

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
