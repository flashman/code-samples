AMBIGUOUS_DNA = {
    "A": ["A"],
    "C": ["C"],
    "G": ["G"],
    "T": ["T"],
    "R": ["A", "G"],
    "N": ["A", "C", "G", "T"],
}


def resolve_ambiguois(sequence: str):
    return _recurse([""], sequence)


def _recurse(seqs: list[str], remaining: str):
    if not remaining:
        return seqs
    else:
        next_seqs = []
        r = remaining[0]
        remaining = remaining[1:]
        for s in seqs:
            for alt in AMBIGUOUS_DNA[r]:
                next_seqs.append(s + alt)

    return _recurse(next_seqs, remaining)


def resolve_ambiguois2(sequence: str):
    ambiguous_bases = [b for b, alts in AMBIGUOUS_DNA.items() if len(alts) > 1]
    out = [sequence]
    i = 0
    for i, s in enumerate(sequence):
        new_out = []
        for seq in out:
            if s in ambiguous_bases:
                for alt in AMBIGUOUS_DNA[s]:
                    new_out.append(seq[:i] + alt + seq[i + 1 :])
            else:
                new_out.append(seq)
        out = new_out
        i += 1

    return out


def resolve_ambiguois3(sequence: str):
    return _recurse3([sequence])


def _recurse3(sequences, i=0):
    if i == len(sequences[0]):
        return sequences
    else:
        next_seqs = []
        for s in sequences:
            for alt in AMBIGUOUS_DNA[s[i]]:
                next_seqs.append(s[:i] + alt + s[i + 1 :])
        return _recurse3(next_seqs, i + 1)


def resolve_ambiguois_dfs(sequence: str):
    return [r for r in _recurse_dfs("", sequence)]


def _recurse_dfs(base, remaining):
    if len(remaining) == 0:
        yield base
    else:
        for alt in AMBIGUOUS_DNA[remaining[0]]:
            new_base = base + alt
            yield from _recurse_dfs(new_base, remaining[1:])


def test_resolve():
    assert resolve_ambiguois2("CCNCCN") == resolve_ambiguois("CCNCCN")


def test_resolve3():
    assert resolve_ambiguois3("CCNCCN") == resolve_ambiguois("CCNCCN")


def test_resolve_dfs():
    assert resolve_ambiguois_dfs("CCNCCN") == resolve_ambiguois("CCNCCN")
