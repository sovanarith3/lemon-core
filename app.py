from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "EcoPulse AI is monitoring your farm!"

@app.route('/advice')
def get_advice():
    return jsonify({"advice": "Conditions are good."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
