import socket
import urllib.request

def get_system_info():
    """מחזיר שם מחשב ו אי פי חיצוני"""
    computer_name = socket.gethostname()
    try:
        external_ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
    except:
        external_ip = "Unknown external IP"

    return {
        "computer_name": computer_name,
        "external_ip": external_ip,
    }

print(get_system_info())
