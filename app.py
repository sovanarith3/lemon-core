from flask import Flask, render_template
import logging
import os

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

@app.route('/')
def index():
    logging.debug("Rendering index page")
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
