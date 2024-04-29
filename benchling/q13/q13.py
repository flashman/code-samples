def find_substrings(s, chars="01", wildcard="?"):
    """
    Given a string s consisting of 0, 1 and ?. The question mark can be either 0 or 1. Find all possible combinations for the string.
    """

    yield from _find_substrings("", s, chars, wildcard)


def _find_substrings(base, remaining, chars, wildcard):
    # Look for next wildcard
    i_wc = remaining.find(wildcard)
    # Base case: There are no wildcards.  Just return the base and whatever was remaining.
    if i_wc == -1:
        yield base + remaining
    else:
        # Swap in each replacement character.
        for c in chars:
            # Create new base from original base plus everything left of the wildcard
            new_base = base + remaining[:i_wc] + c
            new_remaining = remaining[(i_wc + 1) :]
            # Recurse!
            yield from _find_substrings(new_base, new_remaining, chars, wildcard)


def test_find_substrings():
    s = "001?"
    e = ["0010", "0011"]
    o = list(find_substrings(s))
    assert e == o

    s = "?"
    assert ["0", "1"] == list(find_substrings(s))

    s = "0?1?"
    assert ["0010", "0011", "0110", "0111"] == list(find_substrings(s))


test_find_substrings()
