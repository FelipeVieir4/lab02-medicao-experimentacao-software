def kebabize(st):
    res = []
    for c in st:
        if c.isalpha():
            if c.isupper() and res:
                res.append('-')
            res.append(c.lower())
    return "".join(res)
