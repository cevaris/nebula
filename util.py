def spinning_cursor():
    cursor='/-\|'
    i = 0
    while True:
        yield cursor[i]
        i = (i + 1) % len(cursor)