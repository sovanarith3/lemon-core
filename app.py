from flask import Flask, render_template
import logging
import os
import indra

logging.basicConfig(level=logging.DEBUG)
logging.debug("Starting app.py")

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['STATIC_FOLDER'] = 'static'
logging.debug("Flask app initialized")

# Log templates directory contents
templates_dir = os.path.join(app.root_path, 'templates')
logging.debug(f"Templates directory: {templates_dir}")
if os.path.exists(templates_dir):
    logging.debug(f"Templates directory contents: {os.listdir(templates_dir)}")
else:
    logging.error("Templates directory does not exist")

indra_instance = indra.IndraAI()

@app.route('/')
def index():
    status = indra_instance.get_status()
    memory = indra_instance.get_memory()
    logging.debug("Rendering index page")
    return render_template('index.html', status=status, memory=memory)

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
