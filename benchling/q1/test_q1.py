import random
import pytest
import timeit

from q1 import find_matches_v1


def get_random_sequence(aas="ACTG", length=100, num=1000):
    for _ in range(num):
        yield "".join(random.choices(aas, k=length))


def test_find_matches_v1():
    # N = A or T
    sub_sequence = "ACTNG"

    match_seqs = [
        "ACTAG",
        "ACTTG",
        "AAACTTGAA",
    ]

    non_match_seqs = [
        "",
        "AAAAA",
        "ACTCG",
        "ACTGG",
        "ACTNG",
    ]

    assert list(find_matches_v1(match_seqs, sub_sequence)) == match_seqs
    assert list(find_matches_v1(non_match_seqs, sub_sequence)) == []


def test_find_matches_v1_multiple_ambiguous():
    sub_sequence_alt = "NXNXN"
    alt_ambiguous_aa_map = {
        "N": ["A", "T"],
        "X": ["A", "C", "G", "T"],
    }

    match_seqs = [
        "ACTAA",
        "ACAGA",
        "AAACTTGAA",
    ]

    non_match_seqs = [
        "",
        "GG",
        "GGGGGG",
        "asdf",
    ]

    assert (
        list(find_matches_v1(match_seqs, sub_sequence_alt, alt_ambiguous_aa_map))
        == match_seqs
    )
    assert (
        list(find_matches_v1(non_match_seqs, sub_sequence_alt, alt_ambiguous_aa_map))
        == []
    )


def test_find_matches_v1_speed():
    sequences = get_random_sequence(length=10000, num=10000)

    result = timeit.timeit(
        lambda: list(find_matches_v1(sequences, "ACTGGGNNGG")), number=10
    )

    print(result)

    assert result / 10 < 1


# Run pytest as main
if __name__ == "__main__":
    retcode = pytest.main(["-x", "../q1/test_q1.py", "-vv"])
