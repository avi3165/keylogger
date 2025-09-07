import os
from datetime import datetime
import json

BASE_DIR = "logs"

def save_data_with_time(computer_name,dt,window,date,data):
    base_path = "Bacekend\\data"
    folder_name = computer_name
    full_path = os.path.join(base_path, folder_name)
    os.makedirs(full_path, exist_ok=True)
    
    with open(f"Bacekend\\data\\{computer_name}\\{date}.txt", "a", encoding="utf-8") as f:
        f.write(str(dt) + window + data + "\n")

    return ""


def read_text(folder_name,f_date,t_date,date_format):
    all_texts = []
    DATA_PATH = "Bacekend\\data"
    if folder_name in os.listdir(DATA_PATH):
        for file_name in os.listdir(f"{DATA_PATH}\\{folder_name}"):
            if file_name.endswith(".txt"):
                new_name = file_name[:-4]
                try:
                    file_date = datetime.strptime(new_name,date_format)
                    if f_date <= file_date<= t_date:
                        file_path = os.path.join(DATA_PATH,folder_name,file_name)
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
        return result
    result = {
        "machine_name": folder_name,
        "content": all_texts
    }
    return result

def get_machines():
    a = os.listdir("Bacekend\data")
    machines = []
    for i in a:
        machine = {"name":i}
        machines.append(machine)
    return machines
