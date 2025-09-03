import os
from datetime import datetime

def save_data_with_time(base_dir, data):
    """
    שומר מידע בקובץ לפי שעה, ובתיקייה לפי תאריך.
    :param base_dir: תקיית הבסיס (לדוגמה: "logs")
    :param data: מחרוזת לכתיבה לקובץ
    """
    # מקבלים את התאריך והשעה הנוכחיים
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")   # לדוגמה: 2025-09-03
    hour_str = now.strftime("%H")         # לדוגמה: 14

    # יוצרים תקייה חדשה לפי תאריך אם לא קיימת
    date_dir = os.path.join(base_dir, date_str)
    os.makedirs(date_dir, exist_ok=True)

    # שם הקובץ לפי שעה
    file_name = f"{hour_str}.txt"
    file_path = os.path.join(date_dir, file_name)

    # כותבים את המידע לקובץ (נוסיף שורה חדשה)
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(data + "\n")

    return file_path

# דוגמה לשימוש
if __name__ == "__main__":
    path = save_data_with_time("logs", "שלום עולם")
    print(f"נשמר בקובץ: {path}")

