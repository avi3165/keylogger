import os
from datetime import datetime
import json

BASE_DIR = "logs"

def save_data_with_time(computer_name,date,data):
    base_path = "Bacekend\\data"
    folder_name = computer_name
    full_path = os.path.join(base_path, folder_name)
    os.makedirs(full_path, exist_ok=True)
    
    with open(f"Bacekend\\data\\{computer_name}\\{date}.txt", "a", encoding="utf-8") as f:
        f.write(data + "\n")

    return ""


def read_text(folder_name,f_date,t_date,date_format = "%Y-%m-%d"):
    f_date = datetime.strptime(f_date,date_format)
    t_date = datetime.strptime(t_date,date_format)
    all_texts = []
    data_path = "Bacekend\\data"
    if folder_name in os.listdir(data_path):
        for file_name in os.listdir(f"{data_path}\\{folder_name}"):
            if file_name.endswith(".txt"):
                new_name = file_name[:-4]
                try:
                    file_date = datetime.strptime(new_name,date_format)
                    if f_date <= file_date<= t_date:
                        file_path = os.path.join(data_path,folder_name,file_name)
                        with open(file_path,"r") as f:
                            text = f.read()
                            all_texts.append(text)
                except ValueError:
                    continue
    if not all_texts:
        result = {
        "machine_name": "ERROR",
        "content": "NO DATA"
    }
        return json.dumps(result)
    result = {
        "machine_name": folder_name,
        "content": all_texts
    }
    return json.dumps(result)

def get_machines():
    a = os.listdir("Bacekend\data")
    machines = []
    for i in a:
        machine = {"name":i}
        machines.append(machine)
    return json.dumps(machines)
