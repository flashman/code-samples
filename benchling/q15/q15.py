"""
Given a list of intervals, create a new list of intervals where all overlapping or adjacent
intervals are combined.


The problem is easy for two, just make sure there in the correct order and check
- L.r < R.l


For more than two, say (1,3), (2,4), (2,5), (5, 6), (7,8)
Does the merge order matter? No it shouldn't
Can we merge from right to left. Yes
From what ever is merged we only need to worry about the last processed and the next.

"""

from random import shuffle


def resolve(intervals):
    # Exit early.
    if len(intervals) < 2:
        return intervals

    # Just sort once.
    intervals = sorted(intervals)

    # Initialize resolved.
    resolved_intervals = [intervals.pop(0)]

    # Work from left to right.
    for interval in intervals:
        last = resolved_intervals.pop()
        resolved = resolve_pair(last, interval)
        resolved_intervals.extend(resolved)

    return resolved_intervals


def resolve_pair(existing, other):
    existing, other = sorted([existing, other])
    if existing[1] >= other[0]:
        return [(existing[0], other[1])]
    else:
        return [existing, other]


def test_resolve_pair_overlap():
    assert [(1, 4)] == resolve_pair((1, 3), (2, 4))


def test_resolve_pair_no_overlap():
    assert [(1, 3), (4, 5)] == resolve_pair((1, 3), (4, 5))


def test_resolve_pair_oooo():
    assert [(1, 4)] == resolve_pair((2, 4), (1, 3))


def test_resolve_simple():
    assert [(1, 4)] == resolve([(1, 3), (3, 4)])


def test_resolve_example1():
    assert [(1, 6), (7, 8)] == resolve([(1, 3), (2, 4), (2, 5), (5, 6), (7, 8)])


def test_resolve_example1_shuffle():
    intervals = [(1, 3), (2, 4), (2, 5), (5, 6), (7, 8)]
    shuffle(intervals)
    assert [(1, 6), (7, 8)] == resolve(intervals)
