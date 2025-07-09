from flask import Flask, jsonify
import os
from ecopulse import EcoPulse

app = Flask(__name__)
ecopulse = EcoPulse()

@app.route('/')
def home():
    return "EcoPulse AI is monitoring your farm!"

@app.route('/advice')
def get_advice():
    return jsonify({"advice": ecopulse.get_advice()})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
