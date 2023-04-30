i1 = [1, 2, 3, 4, 5, 6, 8, 9]
i2 = [1, 2]
i3 = [1, 3]


def get_chunked(i: list[int], chunked: list[list[int]]):
    chunk = []
    while i:
        a = i.pop()
        if chunk:
            if chunk[-1] - a == 1:
                chunk.append(a)
            else:
                i.append(a)
                i, chunked = get_chunked(i, chunked)
        else:
            chunk.append(a)
    chunked.append(chunk)
    return i, chunked

print(get_chunked(i1, []))
print(get_chunked(i2, []))
print(get_chunked(i3, []))


print([n for chunk in [[6, 5, 4, 3, 2, 1], [9, 8, 10]] for n in chunk if len(chunk)>= 3])