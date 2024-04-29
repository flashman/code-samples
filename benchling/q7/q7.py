"""
Longest Substring Without Repeating Characters - Leetcode 3 - Python
Find the longest substring within one string.  You can delete characters.  Kind of confusing.
"""


def get_longest_substring_without_repeats(sin):
    if not sin:
        return ""

    i = 0
    j = 1
    longest = [i, j]

    while i < len(sin) - (longest[1] - longest[0]):
        # Keep track of last position when repeat is found.
        unique = {sin[i]: i}
        j = i + 1
        while j < len(sin):
            nxt = sin[j]
            # Check if nxt is a repeat.
            if nxt in unique:
                # Check if length of repeat sequence is longer than before.
                if (longest[1] - longest[0]) < (j - i):
                    # Update if so.
                    longest = [i, j]
                # Fast forward to first position after repeat.
                i = unique[nxt] + 1
                # Continue with outer loop.
                break
            else:
                # Otherwise save uniqueness and continue to look for repeat char.
                unique[nxt] = j
                j += 1

        # Handle case of running off end.
        if j == len(sin):
            # Even though we didn't encounter repeat, we could still have the longest
            # Indexes are a little confusing here because j is the right end of the range and
            # notthe
            if (longest[1] - longest[0]) < (j - i):
                longest = [i, j]
            break

    return sin[longest[0] : longest[1]]


def test_get_longest_substing_without_repeats():
    assert "ABCDEF" == get_longest_substring_without_repeats("ABCDEABCDEFABCDE")
    assert "A" == get_longest_substring_without_repeats("A")
    assert "A" == get_longest_substring_without_repeats("AAA")
    assert "ABC" == get_longest_substring_without_repeats("AABCABC")
    assert "ABC" == get_longest_substring_without_repeats("AABCCBC")
    assert "BACD" == get_longest_substring_without_repeats("AABCBACD")


def test_failing():
    assert "ABCD" == get_longest_substring_without_repeats("ABCDDCBAA")


import numpy as np

a = np.fromstring("ACTG", np.char)
print(a)
