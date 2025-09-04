import os
from datetime import datetime
import json

BASE_DIR = "logs"

def save_data_with_time(data):
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")   # לדוגמה: 2025-09-03
    hour_str = now.strftime("%H")         # לדוגמה: 14

    date_dir = os.path.join(BASE_DIR, date_str)
    os.makedirs(date_dir, exist_ok=True)

    file_path = os.path.join(date_dir, f"{hour_str}.txt")

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(data + "\n")

    return file_path


def read_text(folder_name,f_date,t_date,date_format = "%Y-%m-%d"):
    f_date = datetime.strptime(f_date,date_format)
    t_date = datetime.strptime(t_date,date_format)
    all_texts = []
    print(os.getcwd())
    if folder_name in os.listdir(folder_name) :
        for file_name in os.listdir(folder_name):
            if file_name.endswith(".txt"):
                new_name = file_name[:-4]
                try:
                    file_date = datetime.strptime(new_name,date_format)
                    if f_date <= file_date<= t_date:
                        file_path = os.path.join(folder_name,file_name)
                        with open(file_path,"r") as f:
                            text = f.read()
                            all_texts.append(text)
                except ValueError:
                    continue
    if not all_texts:
        result = {
        "machine_name": folder_name,
        "content": "NO DATA"
        }
        return json.dumps(result) 
    result = {
        "machine_name": folder_name,
        "content": all_texts
    }
    return json.dumps(result)

read_text("nn","2025-09-04","2025-09-04")