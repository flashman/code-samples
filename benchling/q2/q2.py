def generate_protein(sequences, protein):
    """
    sequences = {
    'AC': (5, 15),
    'BC': (3, 20),
    'PQ': (15, 22),
    'XY': (22, 35),
    'AB': (20, 32),
    'BT': (9, 13)
    }

    protein = {
    ('AC', 'PQ'): 'P1',
    ('AC','PQ','XY'): 'P2',
    ('BC', 'AB'): 'P3',
    ('BT', 'AC') : 'P4'
    }

    generate_protein => (P1, 5,22), (P2, 5, 35), (P3, 3, 32)
    """

    out = []

    # Iterate over protein components.
    for components, name in protein.items():
        # Get relevant region ranges.
        regions = sorted([sequences[comp] for comp in components])
        # check that end and start of adjacent regions touch.
        if regions and all(r1[1] == r2[0] for r1, r2 in zip(regions[:-1], regions[1:])):
            out.append((name, regions[0][0], regions[-1][1]))

    return out


def test_generate_protein_example():
    sequences = {
        "AC": (5, 15),
        "BC": (3, 20),
        "PQ": (15, 22),
        "XY": (22, 35),
        "AB": (20, 32),
        "BT": (9, 13),
    }

    protein = {
        ("AC", "PQ"): "P1",
        ("AC", "PQ", "XY"): "P2",
        ("BC", "AB"): "P3",
        ("BT", "AC"): "P4",
    }

    expected = [("P1", 5, 22), ("P2", 5, 35), ("P3", 3, 32)]
    out = generate_protein(sequences, protein)

    assert expected == out


def test_generate_protein_simple_cases():
    sequences = {
        "AC": (5, 15),
        "BC": (3, 20),
        "PQ": (15, 22),
        "XY": (22, 35),
        "AB": (20, 32),
        "BT": (9, 13),
    }

    protein = {(): "P1", ("AC",): "P2"}

    expected = [("P2", 5, 15)]
    out = generate_protein(sequences, protein)

    assert expected == out


def test_generate_protein_wrong_order():
    sequences = {
        "AC": (5, 15),
        "BC": (3, 20),
        "PQ": (15, 22),
        "XY": (22, 35),
        "AB": (20, 32),
        "BT": (9, 13),
    }

    protein = {
        ("AC", "XY", "PQ"): "P2",
    }

    assert [("P2", 5, 35)] == generate_protein(sequences, protein)
