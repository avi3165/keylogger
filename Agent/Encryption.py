import base64

# הצפנה במודל אקסור  עם מגוון מפתחות ושימוש בבייס 64  כדי לקבל פלט קריא  #
def encryption(text):
    """הפונקציה עושה הצפנת אקסור ומשתמשת בביס 64 כדי לקבל טקסט קריא"""
    l = [88, 2, 15, 12, 55, 22]
    encrypted = bytearray()
    text_bytes = text.encode('utf-8')

    for i, b in enumerate(text_bytes):
        k = l[i % len(l)]
        encrypted.append(b ^ k)

    return base64.b64encode(encrypted).decode('utf-8')

# תרגום מהצפנה בהתבסס על אותם מפתחות #
def decryption(enc_text):
    """הפונקציה מבצעת תרגום מהצפנה על סמך המפתחות ששימשו להצפנה"""
    l = [88, 2, 15, 12, 55, 22]
    data = base64.b64decode(enc_text)
    decrypted = bytearray()

    for i, b in enumerate(data):
        k = l[i % len(l)]
        decrypted.append(b ^ k)

    return decrypted.decode('utf-8')
# טיפול בליסט או סטרינג שמכיל כמה מילים #
def decrypt_multiple(enc_texts):
    """הפונקציה מבצעת תרגום מהצפנה על סמך המפתחות ששימשו להצפנה"""
    parts = enc_texts.strip().split()
    return ' '.join(decryption(part) for part in parts)

