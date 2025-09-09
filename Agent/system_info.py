import socket
# מחזירה את שם המחשב #
#  ip ניתן להוסיף מידע נוסף כמו #
def get_system_info():
    return {
        "computer_name": socket.gethostname(),
    }
