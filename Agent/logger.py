# logger.py
import requests
import os
# קלאס שמקבל שם קובץ וכתובת שרת #
class Logger:
    def __init__(self, log_file: str, server_url: str):
        self.log_file = log_file
        self.server_url = server_url
   # נסיון כתיבה לקובץ #
    def write_to_file(self, data: str):
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(data)
        except Exception as e:
            print(f"[Error] Writing to file failed: {e}")
    #  jsun נסיון שליחה לשרת במבנה #
    def send_to_server(self, data: dict):
        try:
            response = requests.post(self.server_url, json=data)
            if response.status_code != 200:
                print(f"[Warning] Server responded with status code {response.status_code}")
        except Exception as e:
            print(f"[Error] Sending data to server failed: {e}")
