def encryption(text):
    t = ""
    l = [88, 2, 15, 12]
    for i , v in enumerate(text):
        k = l[ i % (len(l))]
        a = chr(ord(v)^ k)
        t += a
    return t

