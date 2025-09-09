from pynput.keyboard import Key

MODIFIER_KEYS = {
    Key.ctrl_l, Key.ctrl_r,
    Key.alt_l, Key.alt_r,
    Key.shift, Key.shift_l, Key.shift_r,
    Key.cmd, Key.cmd_l, Key.cmd_r
}

def get_modifiers_text(pressed_keys):

    '''הפונקציה מקבלת את המקשים שנלחצו כעת
    ומחזירה רשימה של שמות מקשי קיצור שנלחצו (Ctrl, Alt, Shift וכו')'''

    keys = []
    for key in pressed_keys:
        if key in {Key.ctrl_l, Key.ctrl_r}:
            keys.append("Ctrl")
        elif key in {Key.alt_l, Key.alt_r}:
            keys.append("Alt")
        elif key in {Key.shift, Key.shift_l, Key.shift_r}:
            keys.append("Shift")
        elif key in {Key.cmd, Key.cmd_l, Key.cmd_r}:
            keys.append("Cmd")
    return keys
