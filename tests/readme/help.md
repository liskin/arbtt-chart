<!-- common
    $ . "$TESTDIR"/common.sh
-->

    $ arbtt-chart --help
    usage: arbtt-chart [-h] [--no-stacked] [--subtags] [--totals-re RE]
    
    Plot charts from arbtt-stats to terminal. Expects `arbtt-stats --output-
    format=csv --category=…` or `arbtt-stats --output-format=csv --each-category`
    output on stdin.
    
    options:
      -h, --help      show this help message and exit
      --no-stacked    don't stack bar chart
      --subtags       recognize subtags (separated by '-') and sort them together
      --totals-re RE  totals row regexp, default: ^\(total time\)$
