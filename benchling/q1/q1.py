import re


def find_matches_v1(sequences, sub_sequence, ambiguous_aa_map={"N": ["A", "T"]}):
    """
    input is ACTNG, where N can be A or T. Find all DNA sequences that contain the input.
    identify bugs and places to extend it with new features
    """

    # Construct regex from ambiguous_aa_map
    for amb_aa, aas in ambiguous_aa_map.items():
        amb_aa_re = f"[{''.join(aas)}]"
        sub_sequence = sub_sequence.replace(amb_aa, amb_aa_re)

    for seq in sequences:
        if re.search(sub_sequence, seq):
            yield seq
