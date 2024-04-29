"""
For this question, sequences are defined as tuples, with the first index indicating the name of the sequence, followed by the starting an end index like so:

Sequences

('acG', 0, 5)
('Bf5', 0, 22)
('e5c', 5, 16)
('6a5d', 5, 17)
('7f6c', 2, 13)
('0Pf', 13, 23)
('0f5c', 0, 13)
A protein is defined as one or more sequences with matching start and end indices, for example:

('acG', 0, 5)
or

 ('acG_e5c', 0, 16)
The question is, given a list of gene sequences, find generate all possible proteins.
In the exampe above, the answer would be:

[
('acG', 0, 5)
('Bf5', 0, 22),
('e5c', 5, 16),
('6a5d', 5, 17)
('7f6c', 2, 13),
('0Pf', 13, 23),
('0f5c', 0, 13),
('acG_e5c', 0, 16),
('acG_6a5d', 0, 17),
('7f6c_0Pf', 2, 23),
('0f5c_0Pf', 0, 23),
]
"""


def generate_all_proteins(sequences):
    # Index start positions and share.
    sequence_map = {}
    for s in sequences:
        start = s[1]
        if start in sequence_map:
            sequence_map[start].append(s)
        else:
            sequence_map[start] = [s]
    # Run main generator.
    yield from _generate(sequences, sequence_map)


def _generate(sequences, sequence_map):
    next_sequnces = []
    for seq in sequences:
        yield seq
        end = seq[2]
        if end in sequence_map:
            for next_seq in sequence_map[end]:
                next_sequnces.append(_reduce(seq, next_seq))

    if next_sequnces:
        yield from _generate(next_sequnces, sequence_map)


def _reduce(base, seq):
    return (base[0] + "_" + seq[0], base[1], seq[2])


def test_reduce():
    assert ("a_b", 0, 10) == _reduce(("a", 0, 5), ("b", 5, 10))


def test_generate_all_proteins():
    sequences = [
        ("acG", 0, 5),
        ("Bf5", 0, 22),
        ("e5c", 5, 16),
        ("6a5d", 5, 17),
        ("7f6c", 2, 13),
        ("0Pf", 13, 23),
        ("0f5c", 0, 13),
    ]

    expected = [
        ("acG", 0, 5),
        ("Bf5", 0, 22),
        ("e5c", 5, 16),
        ("6a5d", 5, 17),
        ("7f6c", 2, 13),
        ("0Pf", 13, 23),
        ("0f5c", 0, 13),
        ("acG_e5c", 0, 16),
        ("acG_6a5d", 0, 17),
        ("7f6c_0Pf", 2, 23),
        ("0f5c_0Pf", 0, 23),
    ]

    assert expected == list(generate_all_proteins(sequences))
