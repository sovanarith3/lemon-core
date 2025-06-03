from flask import Flask, render_template
import indra_ai as indra

app = Flask(__name__)

@app.route('/')
def index():
    ai = indra.IndraAI()
    memory = ai.get_memory()
    return render_template('index.html', status="Running", memory=memory)

if __name__ == '__main__':
    import os
    port = int(os.getenv("PORT", 8080))  # Use Railway's PORT or default to 8080
    app.run(host='0.0.0.0', port=port)
