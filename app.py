from flask import Flask, render_template, request, jsonify
from ecopulse import EcoPulse

app = Flask(__name__, template_folder='templates')
ecopulse = EcoPulse()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/advice', methods=['GET', 'POST'])
def get_advice():
    if request.method == 'POST':
        moisture = int(request.form['moisture'])
        temp = int(request.form['temp'])
        advice = ecopulse.get_advice(moisture, temp)
        return jsonify({"advice": advice})
    return jsonify({"advice": ecopulse.get_advice()})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
