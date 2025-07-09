from flask import Flask, render_template
app = Flask(__name__, template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/advice')
def get_advice():
    return {"advice": "Conditions are good."}  # Mock response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
