from types import SimpleNamespace

import arbtt_chart as ac


def test_bar():
    def b(r): return ac.bar(20, 0.5, r)
    assert b(SimpleNamespace(Type='text')) == ""
    assert b(SimpleNamespace(Type='bar', FracAbove=0, Frac=1)) == \
        "██████████▓█████████"
