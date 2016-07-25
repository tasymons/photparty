def fixindex(length, ra, rb, ca, cb):
    test = [ra, rb, ca, cb]
    new = []
    for i in test:
        if i < 0:
            newindex = 0
        elif i > length:
            newindex = length
        else:
            newindex = i
        new.append(newindex)
    if new[0] == new[1]:
        new[1] = 1
    if new[2] == new[3]:
        new[2] = length - 1
    return new[0], new[1], new[2], new[3]