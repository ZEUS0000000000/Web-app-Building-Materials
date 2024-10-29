def stone(a, b, c):
    win = set()
    for i in range(1, b + 1):
        for j in range(a, b + 1):
            if 4 * max(i, j) + min(i, j) == c - 1:
                if i > j:
                    win.add((j, i))
                else:
                    win.add((i, j))
    return win


def two_S(a, b, c, win):
    s = []
    for i in win:
        if i[0] == a:
            if i[1] // 4 * 4 + a > c - 1:
                s.append(i[1])
        else:
            k = i[0] // 4
            if i[0] - 1 == a or (k * 4 == i[0] and k == a):
                s.append(i[1])
    s.sort()
    print(*s)


n = 10
m = 10
stn = 20
res = stone(n, m, stn)
two_S(n, m, stn, res)