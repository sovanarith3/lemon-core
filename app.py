from flask import Flask, render_template, jsonify
import indra_ai as asi  # Renamed to reflect ASI

app = Flask(__name__)

@app.route('/')
def index():
    ai = asi.ASI()
    memory = ai.get_memory()
    return render_template('index.html', status="Running", memory=memory)

@app.route('/roam_auto')
def roam_auto():
    ai = asi.ASI()
    perception_data = ai.perceive_agi()
    return jsonify(perception_data)

@app.route('/simulate')
def simulate():
    ai = asi.ASI()
    perception_data = ai.perceive_agi()
    decision = ai.simulate_decision(perception_data)
    return jsonify(decision)

if __name__ == '__main__':
    import os
    port = int(os.getenv("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
