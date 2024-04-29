"""
Given a string s consisting of digits 0-9 and lowercase English letters a-z.

A string is interesting if you can split it into one or multiple substrings, such that each
substring starts with a number and this number represents the number of characters after it.
Retrun true if string s is intersting, otherwise false.

Base Cases:
abc -> Not interesting
1a -> interesting
2a2 -> interesting



Alg:
Find the next block of numbers

Note that the numbers 2, 23 are both present in 23abc, so we technically need to consider both.

for each number number, get the next n characters, these characters should either end the word, or
be followed by another interesting sub string.

continue until we run out of characters or find an uninteresting combination.

If the former, we have success.
If the latter, we have failure.
"""

import re


def is_interesting(s):
    # Empty string is bad.
    if len(s) == 0:
        return False

    # Find all number looking things.
    match = re.search("\d+", s)

    if not match or match.start() > 0:
        return False

    end = match.end()
    num = match.group()

    # Iterate over possible number end indexes.
    # Eg. for num=34, j = [1, 2]
    for j in range(1, end + 1):
        # Get the number of characters to look at
        d = int(num[:j])

        # Get the substring and remainder.
        substring = s[j : (j + d)]
        remainder = s[(j + d) :]

        # Substring is too short.
        if len(substring) < d:
            continue
        elif len(remainder) == 0:
            return True
        elif not is_interesting(remainder):
            # Remainder with this digit and substring is not interesting.
            continue
        else:
            return True

    # Nothing interesting.
    return False


def test_is_interesting():
    assert is_interesting("2ab")
    assert is_interesting("2131b")
    assert not is_interesting("22131b")
    assert is_interesting("4g12y6hunter")
    assert not is_interesting("abc")
    assert not is_interesting("31ba2a")
    assert is_interesting("0")
    assert not is_interesting("")
    assert is_interesting("129aaaaaaaaaaa3zyx")


print()
test_is_interesting()
