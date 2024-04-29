def permutations(n):
    """
    Display all permutations of the first n characters in the
    alphabet eg ['A' 'B' 'C'  ...] in ascending order.
    """
    charSet = [chr(v) for v in range(65, 65 + n)]
    return _build(charSet)


def _build(charSet, base=""):
    if not charSet:
        yield base
    else:
        for i in range(len(charSet)):
            first = charSet[i]
            remaining = charSet[:i] + charSet[i + 1 :]
            for b in _build(remaining, base + first):
                yield b


print()
for p in permutations(4):
    print(p)
