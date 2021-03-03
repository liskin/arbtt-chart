# arbtt-chart

**Textual chart for [arbtt][], the automatic, rule-based time tracker.**

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
2. Set up some rules. See [Configuring the arbtt categorizer][], [Effective
   Use of Arbtt][], and [sample categorize.cfg for arbtt-graph][].
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

[pipx]: https://github.com/pipxproject/pipx

## Usage

* TODO: `./arbtt_chart.py --help`
* TODO: examples of input and output
* TODO: example of external data source
