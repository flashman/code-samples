def n_similar_v1(ref: str, seqs: list[str], dist=3) -> bool:
    """
    Given a String reference and a list of strings candidates, compute the number of candidate
    sequences that are similar to the reference sequence.

    Two strings are similar if any rotation of the strings are within 3 substitutions of each
    other.

    Examples:

    GAAAAAA and GAAATTT are similar because you could replace the last 3 A's with Ts to get
    from the first to the second

    GAAAAAA and AAATTTG are similar because you could replace the last 3 A's with Ts and
    rotate one character to the left to get from the first string to the second string

    GAAAAAA and GAATTTT are not similar because you need to make at least 4 substitutions to
    get from the first string to the second string.

    Example Input:

    reference: GAAAAAA
    candidates: [GAAATTT, AAATTTG, GAATTTT]

    Output:
    2
    """

    n = 0
    for seq in seqs:
        if len(seq) != len(ref):
            continue
        for i in range(len(seq)):
            rot = seq[i:] + seq[:i]
            d = sum(s != r for s, r in zip(rot, ref))
            if d <= dist:
                n += 1
                break
    return n


def n_similar_v2(ref, seqs, dist=3):
    n = 0
    ln = len(ref)
    for seq in seqs:
        if len(seq) != ln:
            continue
        rot = seq * 2
        for i in range(len(seq)):
            d = sum(s != r for s, r in zip(rot[i : i + ln], ref))
            if d <= dist:
                n += 1
                break

    return n


def test_n_similar_v1():
    reference = "GAAAAAA"
    candidates = ["GAAATTT", "AAATTTG", "GAATTTT"]

    assert n_similar_v1(reference, candidates) == 2


def test_n_similar_v2():
    reference = "GAAAAAA"
    candidates = ["GAAATTT", "AAATTTG", "GAATTTT"]

    assert n_similar_v2(reference, candidates) == 2
