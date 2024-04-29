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

Algorithm:

  Base case:
      text = "ABCD"
      format = {"bold": [(2,3)]}
      action = text[:i]<tag>text[i:j]</tag>text[j:]
      output = AB<b>C</b>D

  Recurse case:
      text = "ABCD"
      format = {"bold":[(1, 3)], "italics":[(2, 4)]}
      action = text[:1] + to_html(text[1:4], )
"""


FORMAT_TO_TAG = {"bold": "b", "italics": "i"}


def to_html(text, fmt):
    # TODO: Fix within-tag ranges. For now assume disjoint.

    # Build an internal representation i.e. data structure of the tags
    # This ideally makes our life easier. Details TBD.
    tags = [{"f": f, "range": (i, j)} for f, ranges in fmt.items() for (i, j) in ranges]

    print()
    print(tags)

    # TODO: Fix between-tag ranges by creating additional disjoint tags when one tag is open when we
    # go to close another.


def fix_tags(left, right):
    left, right = sorted([left, right])
    if left["r"][1] <= right["r"]:
        return (left, right)
    elif right["e"] <= left["s"]:
        return (right, left)


def test_to_html_example():
    text = "ABCDEFGHIJ"
    fmt = {"bold": [(0, 4)], "italics": [(2, 6)]}
    expected = "<b>AB<i>CD</i></b><i>EF</i>GHIJ"

    out = to_html(text, fmt)
    print(out)
