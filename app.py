from flask import Flask, render_template
import logging
import os
import indra

logging.basicConfig(level=logging.DEBUG)
print("Starting app.py")  # Add print
logging.debug("Starting app.py")

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['STATIC_FOLDER'] = 'static'
print("Flask app initialized")  # Add print
logging.debug("Flask app initialized")

# Log templates directory contents
templates_dir = os.path.join(app.root_path, 'templates')
print(f"Templates directory: {templates_dir}")  # Add print
logging.debug(f"Templates directory: {templates_dir}")
if os.path.exists(templates_dir):
    print(f"Templates directory contents: {os.listdir(templates_dir)}")  # Add print
    logging.debug(f"Templates directory contents: {os.listdir(templates_dir)}")
else:
    print("Templates directory does not exist")  # Add print
    logging.error("Templates directory does not exist")

indra_instance = indra.IndraAI()

@app.route('/')
def index():
    status = indra_instance.get_status()
    memory = indra_instance.get_memory()
    print("Rendering index page")  # Add print
    logging.debug("Rendering index page")
    return render_template('index.html', status=status, memory=memory)

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/health')
def health():
    return {"status": "Flask is running"}

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
