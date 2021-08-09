#!/usr/bin/env python3

import argparse
from collections import namedtuple
import curses
from functools import reduce
from io import StringIO
from shutil import get_terminal_size
from sys import stdin
from sys import stdout

import numpy as np  # type: ignore [import]
import pandas as pd  # type: ignore [import]


def read_blank_separated(f):
    return filter(None, (s.strip("\n") for s in f.read().split("\n\n")))


def read_csv(inp):
    def convert_time(t):
        if t.isdigit():
            return pd.to_timedelta(int(t), unit='s')
        else:
            return pd.to_timedelta(t)

    return pd.read_csv(
        StringIO(inp),
        index_col='Tag',
        usecols=['Tag', 'Time'],
        converters={'Time': convert_time}
    )


def has_meaningful_data(table):
    total = table['Time'].sum()
    return not table.empty and not pd.isna(total) and total.total_seconds() > 0


def extract_category(table):
    [category] = table.index.str.extract(r'^([\w-]+):', expand=False).dropna().unique()
    prefix = category + ":"
    return category, table.rename(lambda s: s[len(prefix) if s.startswith(prefix) else 0:])


def load_inputs(csvs):
    inputs = {}
    for csv in csvs:
        table = read_csv(csv)
        if not has_meaningful_data(table):
            continue

        category, table = extract_category(table)
        if category in inputs:
            inputs[category] = inputs[category].add(table, fill_value=pd.Timedelta(0))
        else:
            inputs[category] = table

    return inputs


Preprocessed = namedtuple('Preprocessed', 'category time_sum table table_totals')


def preprocess(category, table, args):
    if args.subtags:
        table = table.set_index(pd.MultiIndex.from_frame(
            table.index.str.extract(r'^(\(.*\)$|\w*)-?(.*)'),
            names=['Tag', 'SubTag']))

    # sort
    table['TimeTag'] = table.groupby(level='Tag').transform('sum')
    table.sort_values(['TimeTag', 'Time'], ascending=False, inplace=True)
    table.drop('TimeTag', axis='columns', inplace=True)

    # separate total(-ish) rows
    totals_m = table.index.get_level_values('Tag').str.contains(args.totals_re)
    table, table_totals = table[~totals_m], table[totals_m]

    time_sum = table['Time'].sum()
    return Preprocessed(category=category, time_sum=time_sum, table=table, table_totals=table_totals)


def blank(df):
    some_name = df.index[0]
    if type(some_name) == tuple:
        name = tuple('' for _ in some_name)
    elif type(some_name) == str:
        name = ''
    else:
        raise Exception(f"blank: unexpected type ({type(some_name)})")

    index = df.index.take([0]).reindex([name])[0]
    return pd.DataFrame({'Time': [''], 'Type': ['text']}, index=index)


def prepare_one_bartable(time_total, prep, args):
    hour_frac = pd.to_timedelta('01:00:00') / time_total

    table = prep.table.assign(Frac=prep.table['Time'] / time_total)
    table['FracAbove'] = table['Frac'].shift(1, fill_value=0).cumsum() if args.stacked else 0
    table['HourFrac'] = hour_frac
    table['Time'] = table['Time'].map(fmt_time)
    table['Type'] = 'bar'

    table_totals = prep.table_totals.assign(Frac=prep.table_totals['Time'] / time_total)
    table_totals['FracAbove'] = 0
    table_totals['HourFrac'] = hour_frac
    table_totals['Time'] = table_totals['Time'].map(fmt_time)
    table_totals['Type'] = 'total_bar'

    blank_line = blank(table)
    header_line1 = blank_line.rename(lambda _: prep.category, level='Tag')
    header_line2 = header_line1.rename(lambda s: f"{'═' * len(s)}", level='Tag')

    if len(table_totals):
        table_totals = pd.concat([blank_line, table_totals])

    return pd.concat([header_line1, header_line2, table, table_totals])


def prepare_bartables(inputs, args):
    preprocessed = [preprocess(category, table, args=args)
                    for category, table in inputs.items()]
    time_total = max(prep.time_sum for prep in preprocessed)

    return reduce(
        lambda a, b: pd.concat([a, blank(a), b]),
        (prepare_one_bartable(time_total, prep, args=args) for prep in preprocessed)
    )


def draw_bartables(width, table):
    for level in table.index.names:
        width -= table.index.get_level_values(level).str.len().max() + 1
    width -= 1

    time_col = table['Time']
    width -= time_col.str.len().max() + 2

    bar_col = table.apply(lambda r: bar(width, r), axis=1)

    return pd.DataFrame({'Time': time_col, 'Bar': bar_col})


def setup_width():
    width, _ = get_terminal_size()
    pd.set_option('display.width', width)
    pd.set_option('max_colwidth', width)
    return width


def fmt_time(td):
    return strfdelta(td, "{hours:02}:{minutes:02}:{seconds:02}")


def strfdelta(tdelta, fmt):
    tdelta = tdelta.to_pytimedelta()
    d = {}
    d['hours'], rem = divmod(tdelta.seconds, 3600)
    d['hours'] += 24 * tdelta.days
    d['minutes'], d['seconds'] = divmod(rem, 60)
    return fmt.format(**d)


def bar(width, r):
    if r.Type == 'text':
        return ''

    # characters
    bar_char_pad = "·"
    bar_chars_left = "▏▎▍▌▋▊▉█"
    bar_chars_right = "▕▐"

    left_pad_width = r.FracAbove * width
    bar_width = r.Frac * width

    # left pad
    left_pad_width_full = int(left_pad_width)
    left_pad_width_sub = int((left_pad_width - left_pad_width_full) * 8)
    left_pad = left_pad_width_full * bar_char_pad

    # bar starts by a right half/eighth block if left pad rounds up
    if left_pad_width_sub > 5:
        bar = bar_chars_right[0]
        bar_width -= 0.25
    elif left_pad_width_sub > 3:
        if bar_width > 0.5:
            bar = bar_chars_right[1]
            bar_width -= 0.5
        else:
            bar = bar_chars_right[0]
            bar_width -= 0.25
    else:
        bar = ""

    # bar body and left partial block
    bar_width = bar_width if bar_width > 0 and len(left_pad) + len(bar) < width else 0
    bar_width_full = int(bar_width)
    bar_width_sub = int((bar_width - bar_width_full) * 8)
    bar += bar_width_full * bar_chars_left[7]
    if bar_width - bar_width_full > 0:
        bar += bar_chars_left[bar_width_sub]

    # right pad
    right_pad_width = width - len(left_pad) - len(bar)
    right_pad = right_pad_width * "·"

    bar = left_pad + bar + right_pad

    # hour markers
    if r.HourFrac * width > 2:
        for hour in np.arange(r.HourFrac, 1, r.HourFrac):
            hour_col = int(hour * width)
            if hour_col < len(bar):
                if bar[hour_col] == bar_char_pad:
                    bar = bar[:hour_col] + '÷' + bar[hour_col+1:]
                elif bar[hour_col] == bar_chars_left[7]:
                    bar = bar[:hour_col] + '▓' + bar[hour_col+1:]

    return bar


def alternating_bg(output):
    if stdout.isatty():
        curses.setupterm()
        if curses.tigetnum("colors") == 256:
            c0 = curses.tigetstr('sgr0').decode()
            c1 = curses.tparm(curses.tigetstr('setab'), 236).decode()
            c2 = curses.tparm(curses.tigetstr('setab'), 232).decode()

            return "\n".join(
                (c1 if i % 2 else c2) + line + c0
                for i, line in enumerate(output.split("\n")))

    return output


def parse_cmdline_args(*args) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="""
        Plot charts from arbtt-stats to terminal.
        Expects `arbtt-stats --output-format=csv --category=…` or
        `arbtt-stats --output-format=csv --each-category` output on stdin.
        """,
    )
    parser.add_argument(
        '--no-stacked', dest='stacked', action='store_false',
        help="don't stack bar chart",
    )
    parser.add_argument(
        '--subtags', dest='subtags', action='store_true',
        help="recognize subtags (separated by '-') and sort them together",
    )
    totals_re_default = r'^\(total time\)$'
    parser.add_argument(
        '--totals-re', dest='totals_re', default=totals_re_default,
        help=f"totals row regexp, default: {totals_re_default}", metavar='RE',
    )
    return parser.parse_args(*args)


def main() -> None:
    args = parse_cmdline_args()

    inputs = load_inputs(read_blank_separated(stdin))
    if not inputs:
        return print('(no meaningful inputs)')

    bartables = prepare_bartables(inputs, args)
    output = draw_bartables(width=setup_width(), table=bartables)
    print(alternating_bg(output.to_string(header=False, index_names=False)))


if __name__ == "__main__":
    main()
