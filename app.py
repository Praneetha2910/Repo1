from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/logs")
def get_logs():
    if not os.path.exists("logs.txt"):
        return jsonify({"data": ""})
    with open("logs.txt", "r") as f:
        data = f.read()
    return jsonify({"data": data})

if __name__ == "__main__":
    app.run(debug=True)
