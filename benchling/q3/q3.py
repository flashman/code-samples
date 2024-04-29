def is_rotation_v1(s1: str, s2: str) -> bool:
    """
    Given two string s1 and s2, check if s1 is a rotated version of s2.

    Example:

    If s1 = "stackoverflow" then the following are some of its rotated versions:

    "tackoverflows"
    "ackoverflowst"
    "overflowstack"
    where as "stackoverflwo" is not a rotated version.
    """

    if len(s1) != len(s2):
        return False

    for i in range(len(s1)):
        if s2 == s1[i:] + s1[:i]:
            return True

    return False


def is_rotation_v2(s1: str, s2: str) -> bool:
    """
    Given two string s1 and s2, check if s1 is a rotated version of s2.

    Example:

    If s1 = "stackoverflow" then the following are some of its rotated versions:

    "tackoverflows"
    "ackoverflowst"
    "overflowstack"
    where as "stackoverflwo" is not a rotated version.
    """
    if len(s1) != len(s2):
        return False

    return s2 in s1 + s1


def canonical_rotation(s1):
    """
    Given a string s1, return the canonical rotation of s1.
    """
    rotations = [s1[i:] + s1[:i] for i in range(len(s1))]
    return min(rotations)


def n_unique_sequences(seqs: list[str]) -> int:
    """
    Given a list of sequences, return the number of unique sequences, allowing rotations.
    """
    if not seqs:
        return 0

    unique = [seqs.pop()]
    while seqs:
        s = seqs.pop()
        if any(is_rotation_v2(s, u) for u in unique):
            continue
        else:
            unique.append(s)

    return len(unique)


def n_unique_sequences_v2(seqs: list[str]) -> int:
    """
    Given a list of sequences, return the number of unique sequences, allowing rotations.
    """
    return len(set(canonical_rotation(s) for s in seqs))


def test_is_rotation_v1():
    assert is_rotation_v1("stackoverflow", "tackoverflows")
    assert is_rotation_v1("stackoverflow", "ackoverflowst")
    assert is_rotation_v1("stackoverflow", "overflowstack")
    assert not is_rotation_v1("stackoverflow", "overstackflow")


def test_is_rotation_v2():
    assert is_rotation_v2("stackoverflow", "tackoverflows")
    assert is_rotation_v2("stackoverflow", "ackoverflowst")
    assert is_rotation_v2("stackoverflow", "overflowstack")
    assert not is_rotation_v2("stackoverflow", "overstackflow")


def test_unique_sequences():
    assert n_unique_sequences(["ACT"]) == 1
    assert n_unique_sequences(["ACT", "TAC"]) == 1
    assert n_unique_sequences(["ACT", "TAC", "CTA"]) == 1
    assert n_unique_sequences(["AAA", "TAC", "ACT"]) == 2
    assert n_unique_sequences(["ACT", "TAC", "AAA"]) == 2


def test_unique_sequences_v2():
    assert n_unique_sequences_v2(["ACT"]) == 1
    assert n_unique_sequences_v2(["ACT", "TAC"]) == 1
    assert n_unique_sequences_v2(["ACT", "TAC", "CTA"]) == 1
    assert n_unique_sequences_v2(["AAA", "TAC", "ACT"]) == 2
    assert n_unique_sequences_v2(["ACT", "TAC", "AAA"]) == 2
