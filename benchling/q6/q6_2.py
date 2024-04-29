"""
Given a string of text and HTML formats to be applied to the string, generate a valid HTML string.

text = 'ABCDEFGHIJ'
format = {
        'bold': [(0,4)],
        'italics': [(2,6)]
}

output = '<b>AB<i>CD</i></b><i>EF</i>GHIJ'

Note: You need to close </i> at index 4 and then add it back in order to have valid HTML tags

Q: Can we assume format inpyts describes valid HMTL?
Q: Can format tags be nested? e.g. <b>AB<b>CD</b>EF<b> --> <b>ABCDEF</b>

Approach
-----------
March from left to right
Add an open tag when we start a formatting interval
Add text while we are in one or more intervals
When we reach the end of an interval for a particular format,
  if the interval is last in, then we can just close it.
  it other intervals have been opened, we need to first close them in reverse order,
    then close the relevant format,
    then reopen the top tags in forward order


"""

from collections import defaultdict


TAGS = {"bold": "b", "italics": "i", "strike": "s"}


def to_html(text, fmt):
    # Organize events so its easy to check if we are entering or leaving one.
    begin_format = defaultdict(list)
    end_format = defaultdict(list)

    for f, intervals in fmt.items():
        # Fix bad interval declarations
        intervals = resolve_intervals(intervals)
        for start, end in intervals:
            e = (start, end, f)
            begin_format[start].append(e)
            end_format[end].append(e)

    # Sort events by longest for cleaner cuts
    begin_format = {
        i: sorted(events, key=lambda e: e[1] - e[0], reverse=True)
        for i, events in begin_format.items()
    }

    # Sort events by longest for cleaner cuts
    end_format = {
        i: sorted(events, key=lambda e: e[1] - e[0], reverse=True)
        for i, events in end_format.items()
    }

    # March forward, god speed.
    html = []
    format_stack = []

    # TODO: Iterate by start event and skip the handle event free regions in aggregate.
    for i, s in enumerate(text):
        # Check if there are tags to close.
        if i in end_format:
            # Find which events we need to remove.
            idxs = sorted([format_stack.index(e) for e in end_format[i]])

            # Pop the stack and save what needs to get added back.
            reopen_stack = []
            j = len(format_stack) - 1
            while j >= min(idxs):
                e = format_stack.pop()
                html.append(close_tag(e))
                if j not in idxs:
                    # Last out will be first to reopen below.
                    reopen_stack.insert(0, e)
                j -= 1

            # Reopen all closed tags.
            for e in reopen_stack:
                format_stack.append(e)
                html.append(open_tag(e))

        # Open new tags and add them to the stack.
        if i in begin_format:
            for e in begin_format[i]:
                # Watch out for already opened tags!
                format_stack.append(e)
                html.append(open_tag(e))

        # Add the next letter after all opening an closing is done.
        html.append(s)

    # Close whatever's still open
    for e in format_stack[::-1]:
        html.append(close_tag(e))

    return "".join(html)


def open_tag(e):
    print("open ", e)
    return f"<{TAGS[e[2]]}>"


def close_tag(e):
    print("close ", e)
    return f"</{TAGS[e[2]]}>"


def resolve_intervals(intervals):
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
        resolved = _resolve_pair(last, interval)
        resolved_intervals.extend(resolved)

    return resolved_intervals


def _resolve_pair(existing, other):
    existing, other = sorted([existing, other])
    if existing[1] >= other[0]:
        return [(existing[0], other[1])]
    else:
        return [existing, other]


def test_simple():
    text = "ABCD"
    fmt = {"bold": [(2, 3)]}
    expected = "AB<b>C</b>D"

    out = to_html(text, fmt)
    assert out == expected


def test_example_case():
    text = "ABCDEFGHIJK"
    fmt = {"bold": [(0, 4)], "italics": [(2, 6)]}
    expected = "<b>AB<i>CD</i></b><i>EF</i>GHIJK"

    out = to_html(text, fmt)
    assert out == expected


def test_interleve():
    text = "ABCDEFGHIJK"
    fmt = {"bold": [(0, 4), (6, 8)], "italics": [(2, 9)]}
    expected = "<b>AB<i>CD</i></b><i>EF<b>GH</b>I</i>JK"

    out = to_html(text, fmt)
    assert out == expected


def test_overlapping_fmt():
    text = "ABCDE"
    fmt = {"bold": [(0, 2), (1, 3)], "italics": [(0, 3), (1, 10)]}
    expected = "<i><b>ABC</b>DE</i>"

    out = to_html(text, fmt)
    assert out == expected


def test_three_fmt():
    text = "ABCDE"
    fmt = {"bold": [(0, 4)], "italics": [(2, 4)], "strike": [(0, 5)]}
    expected = "<s><b>AB<i>CD</i></b>E</s>"

    out = to_html(text, fmt)
    assert out == expected
