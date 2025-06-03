from flask import Flask, render_template, request
import logging
import os
import indra
import random

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

indra_instance = indra.Indra_ai()

@app.route('/')
def index():
    status = indra_instance.get_status()
    memory = indra_instance.get_memory()
    print("Rendering index page")  # Add print
    logging.debug("Rendering index page")
    return render_template('index.html', status=status, memory=memory)

@app.route('/favicon.ico')
def favicon():
    print("Favicon route hit")  # Add print for debugging
    return "Favicon route working", 200

@app.route('/health')
def health():
    return {"status": "Flask is running"}

@app.route('/stats')
def stats():
    return {"visits": indra_instance.get_memory()["visits"]}

@app.route('/explore', methods=['GET'])
def explore():
    url = request.args.get('url', 'https://example.com')  # Default URL if none provided
    result = indra_instance.explore_web(url)
    return result

@app.route('/roam', methods=['GET'])
def roam():
    start_url = request.args.get('url', 'https://en.wikipedia.org/wiki/Artificial_general_intelligence')
    result = indra_instance.explore_web(start_url)
    if 'links' in result and result['links']:
        next_url = random.choice(result['links'])
        return {"current": result, "next_url": next_url}
    return result

@app.route('/roam_next', methods=['GET'])
def roam_next():
    result = indra_instance.roam_next()
    return result

@app.route('/knowledge', methods=['GET'])
def knowledge():
    return indra_instance.knowledge

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
