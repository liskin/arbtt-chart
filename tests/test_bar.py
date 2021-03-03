from types import SimpleNamespace

import arbtt_chart as ac


def test_bar():
    def b(**kwargs): return ac.bar(20, SimpleNamespace(Type='bar', HourFrac=0.5, **kwargs))
    assert ac.bar(20, SimpleNamespace(Type='text')) == ""
    assert b(FracAbove=0,     Frac=1    ) == "██████████▓█████████"
    assert b(FracAbove=0,     Frac=0.5  ) == "██████████÷·········"
    assert b(FracAbove=0,     Frac=0.4  ) == "████████··÷·········"
    assert b(FracAbove=0,     Frac=0.43 ) == "████████▋·÷·········"
    assert b(FracAbove=0.1,   Frac=0.43 ) == "··████████▋·········"
    assert b(FracAbove=0.13,  Frac=0.43 ) == "··▐███████▓▏········"
    assert b(FracAbove=0.145, Frac=0.43 ) == "··▕███████▓▍········"
    assert b(FracAbove=0.1,   Frac=0.01 ) == "··▎·······÷·········"
    assert b(FracAbove=0.125, Frac=0.015) == "··▕▏······÷·········"
    assert b(FracAbove=0.145, Frac=0.01 ) == "··▕·······÷·········"
    assert b(FracAbove=0.125, Frac=0.027) == "··▐▏······÷·········"
