import win32api
import win32gui
import win32process
import ctypes

user32 = ctypes.WinDLL('user32', use_last_error=True)

# מחזירה מידע על פריסת מקלדת בחלון הנוכחי
def get_keyboard_layout(hwnd):
    """הפונקציה מקבלת מזהה חלון מוצאת על סמך זה את קוד התהליך ואזה מוצאת את שפת המקלדת"""
    thread_id, _ = win32process.GetWindowThreadProcessId(hwnd)
    return win32api.GetKeyboardLayout(thread_id)

# מחזירה מידע על איזה חלון פעיל עכשו
def get_active_window_title():
    """הפןנקציה מחזירה את שם החלון ואת המזהה החלון שלו"""
    hwnd = win32gui.GetForegroundWindow()

    return win32gui.GetWindowText(hwnd), hwnd

# מתרגמת קוד מקש וירטואלי  לתו אמיתי #
def get_character_from_vk_code(vk_code, layout):
    """הפונקציה ממפה קוד מקש וירטואלי לקוד סריקה לפי פריסת המקלדת.
       הפרמטרים הם: קוד המקשים, סוג המיפוי (כאן 0 – מווירטואלי לסריקה), ופריסת המקלדת.
       הפונקציה מחזירה את קוד הסריקה המתאים למקש הפיזי לפי הפריסה.
       כך אפשר לזהות במדויק את המקש שנלחץ לפי שפת המקלדת."""
    scan_code = user32.MapVirtualKeyExW(vk_code, 0, layout)
    # יוצרים מערך של 256 בתים שמייצג את מצב כל מקשי המקלדת#
    key_state = (ctypes.c_ubyte * 256)()
    # קוראים את מצב המקלדת הנוכחי (כל המקשים) ומאחסנים אותו במערך #
    user32.GetKeyboardState(ctypes.byref(key_state))
    # יוצרים מאגר  של 5 תווים שבו הפונקציה תכניס את התווים המתקבלים מהמרת המקשים #
    buffer = ctypes.create_unicode_buffer(5)
    # קוראים לפונקציה עם כל הפרמטרים #
    result = user32.ToUnicodeEx(vk_code, scan_code, key_state, buffer, len(buffer), 0, layout)
    return buffer.value if result > 0 else ''

