# arbtt-chart

**Textual chart for [arbtt][], the automatic, rule-based time tracker.**

[![PyPI Python Version badge](https://img.shields.io/pypi/pyversions/arbtt-chart)](https://pypi.org/project/arbtt-chart/)
[![PyPI Version badge](https://img.shields.io/pypi/v/arbtt-chart)](https://pypi.org/project/arbtt-chart/)
![License badge](https://img.shields.io/github/license/liskin/arbtt-chart)

Similar to [arbtt-graph][], just in plain monospace text.

![demo](https://user-images.githubusercontent.com/300342/109856066-57afba80-7c59-11eb-8771-9612ce478945.png)

(The above screenshot is generated using my [liskin-arbtt-stats][] which
provides a few handy commands and combines data from multiple X sessions and
Strava.)

Raw `arbtt-stats` output for the same time period looks something like this:

![arbtt-stats](https://user-images.githubusercontent.com/300342/109858182-caba3080-7c5b-11eb-890e-5bb9179bbd00.png)

[arbtt]: http://arbtt.nomeata.de/
[arbtt-graph]: https://github.com/rejuvyesh/arbtt-graph
[liskin-arbtt-stats]: https://github.com/liskin/dotfiles/blob/home/bin/liskin-arbtt-stats

## Getting started

1. [Install arbtt](http://arbtt.nomeata.de/#install) and make sure
   `arbtt-capture` runs in your graphical login session.

2. Configure arbtt rules in `~/.arbtt/categorize.cfg`.
   See [Configuring the arbtt categorizer][], [Effective Use of Arbtt][], and
   [sample categorize.cfg for arbtt-graph][].

3. [Install arbtt-chart](#installation).

4. Try `arbtt-stats --output-format=csv --each-category | arbtt-chart` or
   `arbtt-stats --output-format=csv --category=Graph | arbtt-chart`

[Configuring the arbtt categorizer]: http://arbtt.nomeata.de/doc/users_guide/configuration.html
[Effective Use of Arbtt]: http://arbtt.nomeata.de/doc/users_guide/effective-use.html
[sample categorize.cfg for arbtt-graph]: https://github.com/rejuvyesh/arbtt-graph/blob/master/categorize.cfg

## Installation

Using [pipx][]:

```
pipx ensurepath
pipx install git+https://github.com/liskin/arbtt-chart
```

To keep a local git clone around:

```
git clone https://github.com/liskin/arbtt-chart
make -C arbtt-chart pipx
```

Alternatively, if you don't need the isolated virtualenv that [pipx][]
provides, feel free to just:

```
pip install git+https://github.com/liskin/arbtt-chart
```

Or, since the only dependency is [pandas][], you can just `sudo apt install
python3-pandas` and run `arbtt_chart.py` directly. :-)

[pipx]: https://github.com/pipxproject/pipx
[pandas]: https://pandas.pydata.org/

## Usage

    $ arbtt-chart --help
    usage: arbtt-chart [-h] [--no-stacked] [--subtags] [--totals-re RE]
    
    Plot charts from arbtt-stats to terminal. Expects `arbtt-stats --output-
    format=csv --category=…` or `arbtt-stats --output-format=csv --each-category`
    output on stdin.
    
    optional arguments:
      -h, --help      show this help message and exit
      --no-stacked    don't stack bar chart
      --subtags       recognize subtags (separated by '-') and sort them together
      --totals-re RE  totals row regexp, default: ^\(total time\)$

## Examples

### single category

```
​$ arbtt-stats --filter='$date >= 2021-03-0220:00 && $date < 2021-03-0303:00' \
​>             --min-percentage=2 --category=Activity --output-format=csv \
​> | arbtt-chart
​Activity                                                                        
​════════                                                                        
​Proj-arbttⁱ          03:11:40  ███████████▓██████████▓██████████▓██▏········÷···
​Chat                 00:30:20  ···········÷··········÷··········÷··█████▊···÷···
​(8 entries omitted)  00:15:40  ···········÷··········÷··········÷·······▕██▊÷···
​Web-Social           00:08:20  ···········÷··········÷··········÷··········▐▓▏··
​Web-otherⁱ           00:06:40  ···········÷··········÷··········÷···········÷█▍·
​Web-HN               00:06:20  ···········÷··········÷··········÷···········÷·▐▊
​(unmatched time)     00:01:20  ···········÷··········÷··········÷···········÷··▕
​                                                                                
​(total time)         04:20:20  ███████████▓██████████▓██████████▓███████████▓███
```

### single category, subtags

```
​$ arbtt-stats --filter='$date >= 2021-03-0220:00 && $date < 2021-03-0303:00' \
​>             --min-percentage=2 --category=Activity --output-format=csv \
​> | arbtt-chart --subtags
​Activity                                                                        
​════════                                                                        
​Proj                arbttⁱ  03:11:40  █████████▓█████████▓█████████▓█·······÷···
​Chat                        00:30:20  ·········÷·········÷·········÷▕████▊··÷···
​Web                 Social  00:08:20  ·········÷·········÷·········÷·····▕█▏÷···
​                    otherⁱ  00:06:40  ·········÷·········÷·········÷·······█▏···
​                    HN      00:06:20  ·········÷·········÷·········÷········▓▏··
​(8 entries omitted)         00:15:40  ·········÷·········÷·········÷········÷██▋
​(unmatched time)            00:01:20  ·········÷·········÷·········÷········÷··▕
​                                                                                
​(total time)                04:20:20  █████████▓█████████▓█████████▓████████▓███
```

### multiple categories

```
​$ arbtt-stats --filter='$date >= 2021-03-0220:00 && $date < 2021-03-0303:00' \
​>             --min-percentage=2 --each-category --output-format=csv \
​> | arbtt-chart
​Activity                                                                        
​════════                                                                        
​Proj-arbttⁱ          03:11:40  ███████████▓██████████▓██████████▓██▏········÷···
​Chat                 00:30:20  ···········÷··········÷··········÷··█████▊···÷···
​(8 entries omitted)  00:15:40  ···········÷··········÷··········÷·······▕██▊÷···
​Web-Social           00:08:20  ···········÷··········÷··········÷··········▐▓▏··
​Web-otherⁱ           00:06:40  ···········÷··········÷··········÷···········÷█▍·
​Web-HN               00:06:20  ···········÷··········÷··········÷···········÷·▐▊
​(unmatched time)     00:01:20  ···········÷··········÷··········÷···········÷··▕
​                                                                                
​(total time)         04:20:20  ███████████▓██████████▓██████████▓███████████▓███
​                                                                                
​Desktop                                                                         
​═══════                                                                         
​4_arbtt              02:21:40  ███████████▓██████████▓███▊······÷···········÷···
​6_arbtt_web          00:50:20  ···········÷··········÷···▐██████▓██·········÷···
​1_irc                00:34:00  ···········÷··········÷··········÷··██████▌··÷···
​2_web                00:34:00  ···········÷··········÷··········÷········▐██▓███
​(1 entries omitted)  00:00:20  ···········÷··········÷··········÷···········÷··▕
​                                                                                
​(total time)         04:20:20  ███████████▓██████████▓██████████▓███████████▓███
​                                                                                
​Program                                                                         
​═══════                                                                         
​urxvt                02:38:00  ███████████▓██████████▓██████▊···÷···········÷···
​google-chrome        01:21:40  ···········÷··········÷······▐███▓██████████▉÷···
​app_element_io       00:14:40  ···········÷··········÷··········÷···········▓█▉·
​(3 entries omitted)  00:06:00  ···········÷··········÷··········÷···········÷·▕█
​                                                                                
​(total time)         04:20:20  ███████████▓██████████▓██████████▓███████████▓███
```

### custom inputs

    $ arbtt-chart --totals-re='^\(' <<END
    > Tag,Time
    > Act:Work,02:30:00
    > Act:Social,01:20:00
    > Act:Mail,00:20:00
    > Act:Movie,01:30:00
    > (screen),05:40:00
    > 
    > Tag,Time
    > Act:Sport,3600
    > Act:Commute,1800
    > (outside),5400
    > END
    Act                                                                             
    ═══                                                                             
    Work       02:30:00  ████████▓███████▓███▋···÷·······÷········÷·······÷·······÷·
    Movie      01:30:00  ········÷·······÷···▐███▓███████▉········÷·······÷·······÷·
    Social     01:20:00  ········÷·······÷·······÷·······▕████████▓█▊·····÷·······÷·
    Sport      01:00:00  ········÷·······÷·······÷·······÷········÷·▕█████▓██·····÷·
    Commute    00:30:00  ········÷·······÷·······÷·······÷········÷·······÷··████▏÷·
    Mail       00:20:00  ········÷·······÷·······÷·······÷········÷·······÷······█▓▊
                                                                                    
    (screen)   05:40:00  ████████▓███████▓███████▓███████▓████████▓████▊··÷·······÷·
    (outside)  01:30:00  ████████▓███▍···÷·······÷·······÷········÷·······÷·······÷·

### custom inputs, multiple tables at same scale

    $ arbtt-chart <<END
    > Tag,Time
    > Screen:Work,02:30:00
    > Screen:Social,01:20:00
    > Screen:Mail,00:20:00
    > Screen:Movie,01:30:00
    > (total time),05:40:00
    > 
    > Tag,Time
    > Outside:Sport,3600
    > Outside:Commute,1800
    > (total time),5400
    > END
    Screen                                                                          
    ══════                                                                          
    Work          02:30:00  █████████▓█████████▓████▊····÷·········÷·········÷······
    Movie         01:30:00  ·········÷·········÷····▐████▓█████████▍·········÷······
    Social        01:20:00  ·········÷·········÷·········÷·········▐█████████▓██▊···
    Mail          00:20:00  ·········÷·········÷·········÷·········÷·········÷··▐██▉
                                                                                    
    (total time)  05:40:00  █████████▓█████████▓█████████▓█████████▓█████████▓██████
                                                                                    
    Outside                                                                         
    ═══════                                                                         
    Sport         01:00:00  █████████▓·········÷·········÷·········÷·········÷······
    Commute       00:30:00  ·········▕████▊····÷·········÷·········÷·········÷······
                                                                                    
    (total time)  01:30:00  █████████▓████▉····÷·········÷·········÷·········÷······
