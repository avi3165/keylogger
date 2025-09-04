def encryption(text):
    t = ""
    l = [6]
    for i , v in enumerate(text):
        k = l[ i % (len(l))]
        a = chr(ord(v)^ k)
        t += a
    return t

