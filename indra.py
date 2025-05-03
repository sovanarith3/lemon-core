from flask import Flask, jsonify, request

# Create Flask app instance
app = Flask(__name__)

# Define a simple home route
@app.route('/')
def home():
    return "Indra is online and working!"

# Example route with parameters
@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.json
    return jsonify({
        "you_sent": data
    })

# Optional: more routes or functions can go here
