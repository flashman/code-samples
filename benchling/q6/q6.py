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

Strategy
----------
populate position -> format data model

  eg [['b'],['b'],['b', 'i'], ['b', 'i'], ['i'], ['i']]

add an empty string "" and [] format entry at the end to handle

iterate through positions:
  * identify start format event by presence of new format
    * add format to format stack
    * open new format tag
    * add next letter
  * identify end format events by absence of current format in stack
    * remove newer formats from the stack and save them for later
    * remove the target formats from the format stack
    * close the target format tags in reverse order
    * add back end of format stack
    * reopen end of format stack
    # add next letter
  * else just add the letter

After the last





"""


TAGS = {"bold": "b", "italics": "i", "strike": "s"}


def to_html_v1(raw, fmt):
    # Sort fmt by size.
    order = [
        k
        for k, vals in sorted(
            fmt.items(),
            key=lambda f: max(end - start for start, end in f[1]),
            reverse=True,
        )
    ]
    fmt = {k: fmt[k] for k in order}

    # Index format by position.
    position_fmt = [[] for i in range(len(raw))]
    for f, rngs in fmt.items():
        for rng in rngs:
            for i in range(*rng):
                if i < len(raw):
                    position_fmt[i].append(f)

    # Assemble final html here.
    html = []

    # Keep stack of opened tags.
    active_formats = []

    for c, fmt in zip(raw, position_fmt):
        # Close inactive formatting
        remove_formats = [active for active in active_formats if active not in fmt]
        if remove_formats:
            af_min_index = min(active_formats.index(f) for f in remove_formats)

            # Close everthing down to af_min_index starting from end.
            remove_formats = active_formats[af_min_index:]
            active_formats = active_formats[:af_min_index]
            for af in remove_formats[::-1]:
                html.append(f"</{TAGS[af]}>")

        # Open newly active formatting
        new_formats = [f for f in fmt if f not in active_formats]
        if new_formats:
            active_formats.extend(new_formats)
            for nf in new_formats:
                html.append(f"<{TAGS[nf]}>")

        # Add character
        html.append(c)

    # Close all active formats.
    if active_formats:
        for af in active_formats[::-1]:
            html.append(f"</{TAGS[af]}>")

    return "".join(html)


def test_simple():
    text = "ABCD"
    fmt = {"bold": [(2, 3)]}
    expected = "AB<b>C</b>D"

    out = to_html_v1(text, fmt)
    assert out == expected


def test_example_case():
    text = "ABCDEFGHIJK"
    fmt = {"bold": [(0, 4)], "italics": [(2, 6)]}
    expected = "<b>AB<i>CD</i></b><i>EF</i>GHIJK"

    out = to_html_v1(text, fmt)
    assert out == expected


def test_interleve():
    text = "ABCDEFGHIJK"
    fmt = {"bold": [(0, 4), (6, 8)], "italics": [(2, 9)]}
    expected = "<b>AB<i>CD</i></b><i>EF<b>GH</b>I</i>JK"

    out = to_html_v1(text, fmt)
    assert out == expected


def test_overlapping_fmt():
    text = "ABCDE"
    fmt = {"bold": [(0, 2), (1, 3)], "italics": [(0, 3), (1, 10)]}
    expected = "<i><b>ABC</b>DE</i>"

    out = to_html_v1(text, fmt)
    assert out == expected


def test_three_fmt():
    text = "ABCDE"
    fmt = {"bold": [(0, 4)], "italics": [(2, 4)], "strike": [(0, 5)]}
    expected = "<s><b>AB<i>CD</i></b>E</s>"

    out = to_html_v1(text, fmt)
    assert out == expected
