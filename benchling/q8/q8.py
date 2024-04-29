"""
187. Repeated DNA Sequences
Medium
3.2K
507
Companies
The DNA sequence is composed of a series of nucleotides abbreviated as 'A', 'C', 'G', and 'T'.

For example, "ACGAATTCCG" is a DNA sequence.
When studying DNA, it is useful to identify repeated sequences within the DNA.

Given a string s that represents a DNA sequence, return all the 10-letter-long sequences (substrings) that occur more than once in a DNA molecule. You may return the answer in any order.



Example 1:

Input: s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
Output: ["AAAAACCCCC","CCCCCAAAAA"]
Example 2:

Input: s = "AAAAAAAAAAAAA"
Output: ["AAAAAAAAAA"]
"""


def get_repeat_regions(sequence, n=10):
    repeats = set()
    for i in range(len(sequence) - n):
        s = sequence[i : i + n]
        if s in sequence[i + 1 :]:
            repeats.add(s)

    return list(repeats)


def test_get_repeat_regions_ex1():
    sin = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
    sout = ["AAAAACCCCC", "CCCCCAAAAA"]

    assert sout == get_repeat_regions(sin)


def test_get_repeat_regions_ex2():
    sin = "AAAAAAAAAAAAA"
    sout = ["AAAAAAAAAA"]

    assert sout == get_repeat_regions(sin)


def test_get_repeat_regions_others():
    sin = "ACTACTACTAAAAAA"
    sout = ["ACT", "CTA", "TAC", "AAA"]

    assert sout == get_repeat_regions(sin, 3)
