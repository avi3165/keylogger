import base64


def encryption(text):
    l = [88, 2, 15, 12, 55, 22]
    encrypted = bytearray()
    text_bytes = text.encode('utf-8')

    for i, b in enumerate(text_bytes):
        k = l[i % len(l)]
        encrypted.append(b ^ k)

    return base64.b64encode(encrypted).decode('utf-8')


def decryption(enc_text):
    l = [88, 2, 15, 12, 55, 22]
    data = base64.b64decode(enc_text)
    decrypted = bytearray()

    for i, b in enumerate(data):
        k = l[i % len(l)]
        decrypted.append(b ^ k)

    return decrypted.decode('utf-8')

def decrypt_multiple(enc_texts):
    parts = enc_texts.strip().split()
    return ' '.join(decryption(part) for part in parts)



