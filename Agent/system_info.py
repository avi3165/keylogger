import socket

def get_system_info():
    return {
        "computer_name": socket.gethostname(),
    }
