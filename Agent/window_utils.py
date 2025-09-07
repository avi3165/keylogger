import win32api
import win32gui
import win32process
import ctypes

user32 = ctypes.WinDLL('user32', use_last_error=True)
# מחזירה מידע על פריסת מקלדת בחלון הנוכחי #
def get_keyboard_layout(hwnd):
    thread_id, _ = win32process.GetWindowThreadProcessId(hwnd)
    return win32api.GetKeyboardLayout(thread_id)
# מחזירה מידע על איזה חלון פעיל עכשו #
def get_active_window_title():
    hwnd = win32gui.GetForegroundWindow()
    return win32gui.GetWindowText(hwnd), hwnd
# מחזירה תו ממשי בהתאם לשפת מקלדת לפי קוד המקש #
def get_character_from_vk_code(vk_code, layout):
    scan_code = user32.MapVirtualKeyExW(vk_code, 0, layout)
    key_state = (ctypes.c_ubyte * 256)()
    buffer = ctypes.create_unicode_buffer(5)
    result = user32.ToUnicodeEx(vk_code, scan_code, key_state, buffer, len(buffer), 0, layout)
    return buffer.value if result > 0 else ''
