import io
import textwrap

import pandas as pd  # type: ignore [import]
import pandas.testing as pdt  # type: ignore [import]
import pytest  # type: ignore [import]

import arbtt_chart as ac


def test_read_blank_separated_stdin():
    def r(i): return list(ac.read_blank_separated(io.StringIO(i)))
    assert r("") == []
    assert r("a\nb\n") == ["a\nb"]
    assert r("a\n\nb\n\n") == ["a", "b"]
    assert r("a\n\n\nb\n\n\n") == ["a", "b"]
    assert r("a\n\n\n\nb\n\n\n\n") == ["a", "b"]


def test_load_inputs():
    def ld(csvs): return ac.load_inputs(textwrap.dedent(csv.strip("\n")) for csv in csvs)

    # no meaningful data
    assert ld(["""
               Tag,Time
               """]) == {}
    assert ld(["""
               Tag,Time
               _,00:00:00
               """]) == {}

    # single entry
    i = ld(["""
            Tag,Time
            a:y,00:01:00
            """])
    assert list(i.keys()) == ['a']
    pdt.assert_frame_equal(
        i['a'],
        pd.DataFrame(
            {'Time': [pd.to_timedelta('00:01:00')]},
            index=pd.Index(['y'], name='Tag'),
        ),
    )

    # one category
    i = ld(["""
            Tag,Time
            a:y,00:01:00
            a:z,00:02:00
            """])
    assert list(i.keys()) == ['a']
    pdt.assert_frame_equal(
        i['a'],
        pd.DataFrame(
            {'Time': [pd.to_timedelta('00:01:00'), pd.to_timedelta('00:02:00')]},
            index=pd.Index(['y', 'z'], name='Tag'),
        ),
    )

    # one category and totals
    i = ld(["""
            Tag,Time
            a:y,00:01:00
            z,00:02:00
            """])
    assert list(i.keys()) == ['a']
    pdt.assert_frame_equal(
        i['a'],
        pd.DataFrame(
            {'Time': [pd.to_timedelta(t) for t in ['00:01:00', '00:02:00']]},
            index=pd.Index(['y', 'z'], name='Tag'),
        ),
    )

    # different categories
    with pytest.raises(ValueError):
        ld(["""
            Tag,Time
            a:y,00:01:00
            b:z,00:02:00
            """])

    # time in seconds
    i = ld(["""
            Tag,Time
            a:y,180
            """])
    assert list(i.keys()) == ['a']
    pdt.assert_frame_equal(
        i['a'],
        pd.DataFrame(
            {'Time': [pd.to_timedelta('00:03:00')]},
            index=pd.Index(['y'], name='Tag'),
        ),
    )

    # two inputs, one category
    i = ld(["""
            Tag,Time
            a:y,00:01:00
            a:z,00:02:00
            """,
            """
            Tag,Time
            a:x,00:03:00
            a:z,00:04:00
            """,
            ])
    assert list(i.keys()) == ['a']
    pdt.assert_frame_equal(
        i['a'],
        pd.DataFrame(
            {'Time': [pd.to_timedelta(t) for t in ['00:03:00', '00:01:00', '00:06:00']]},
            index=pd.Index(['x', 'y', 'z'], name='Tag'),
        ),
    )

    # two inputs, two categories
    i = ld(["""
            Tag,Time
            a:y,00:01:00
            a:z,00:02:00
            """,
            """
            Tag,Time
            b:x,00:03:00
            b:z,00:04:00
            """,
            ])
    assert list(i.keys()) == ['a', 'b']
    pdt.assert_frame_equal(
        i['a'],
        pd.DataFrame(
            {'Time': [pd.to_timedelta(t) for t in ['00:01:00', '00:02:00']]},
            index=pd.Index(['y', 'z'], name='Tag'),
        ),
    )
    pdt.assert_frame_equal(
        i['b'],
        pd.DataFrame(
            {'Time': [pd.to_timedelta(t) for t in ['00:03:00', '00:04:00']]},
            index=pd.Index(['x', 'z'], name='Tag'),
        ),
    )
