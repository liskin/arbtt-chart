import textwrap

import pandas as pd  # type: ignore [import]
import pandas.testing as pdt  # type: ignore [import]

import arbtt_chart as ac


def ld(csvs):
    return ac.load_inputs(textwrap.dedent(csv.strip("\n")) for csv in csvs)


def test_prepare():
    def prep(csvs, args=[]):
        args = ac.parse_cmdline_args(args)
        return ac.prepare_bartables(ld(csvs), args)

    # one category and totals
    in1 = """
        Tag,Time
        a:x-y,00:01:00
        (unmatched time),00:02:00
        (total time),00:03:00
        """
    out1 = pd.DataFrame(
        {'Time': ['', '', '00:02:00', '00:01:00', '', '00:03:00'],
         'Type': ['text', 'text', 'bar', 'bar', 'text', 'total_bar'],
         'Frac': [None, None, 2/3, 1/3, None, 1],
         'FracAbove': [None, None, 0, 2/3, None, 0],
         'HourFrac': [None, None, 20, 20, None, 20]},
        index=pd.Index(['a', '═', '(unmatched time)', 'x-y', '', '(total time)'], name='Tag'))
    pdt.assert_frame_equal(prep([in1]), out1)

    # same, different totals
    in1_totals = """
        Tag,Time
        a:x-y,00:01:00
        (unmatched),00:02:00
        (screen),00:03:00
        """
    out1_totals = out1.set_index(
        pd.Index(['a', '═', '(unmatched)', 'x-y', '', '(screen)'], name='Tag'))
    pdt.assert_frame_equal(
        prep([in1_totals], args=["--totals-re", "^\\(screen"]),
        out1_totals)

    # same, subtags
    out1_subtags = out1.set_index(
        pd.MultiIndex.from_tuples(
            [('a', ''), ('═', ''), ('(unmatched time)', ''), ('x', 'y'), ('', ''), ('(total time)', '')],
            names=['Tag', 'SubTag']))
    pdt.assert_frame_equal(prep([in1], args=["--subtags"]), out1_subtags)

    # two categories and totals
    in2 = """
        Tag,Time
        b:z,00:01:00
        (unmatched time),00:02:00
        (total time),00:03:00
        """
    blank = pd.DataFrame(
        {'Time': [''], 'Type': ['text'], 'Frac': [None], 'FracAbove': [None], 'HourFrac': [None]},
        index=pd.Index([''], name='Tag'))
    out2 = out1.set_index(
        pd.Index(['b', '═', '(unmatched time)', 'z', '', '(total time)'], name='Tag'))
    pdt.assert_frame_equal(prep([in1, in2]), pd.concat([out1, blank, out2]))

    # three categories, subtags
    in3 = """
        Tag,Time
        c:z,00:01:00
        (unmatched time),00:02:00
        (total time),00:03:00
        """
    out2_subtags = out1.set_index(
        pd.MultiIndex.from_tuples(
            [('b', ''), ('═', ''), ('(unmatched time)', ''), ('z', ''), ('', ''), ('(total time)', '')],
            names=['Tag', 'SubTag']))
    out3_subtags = out1.set_index(
        pd.MultiIndex.from_tuples(
            [('c', ''), ('═', ''), ('(unmatched time)', ''), ('z', ''), ('', ''), ('(total time)', '')],
            names=['Tag', 'SubTag']))
    blank_subtags = blank.set_index(pd.MultiIndex.from_tuples([('', '')], names=['Tag', 'SubTag']))
    pdt.assert_frame_equal(
        prep([in1, in2, in3], args=["--subtags"]),
        pd.concat([out1_subtags, blank_subtags, out2_subtags, blank_subtags, out3_subtags]))
