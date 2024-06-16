# arbtt-chart

[![PyPI Python Version badge](https://img.shields.io/pypi/pyversions/arbtt-chart)](https://pypi.org/project/arbtt-chart/)
[![PyPI Version badge](https://img.shields.io/pypi/v/arbtt-chart)](https://pypi.org/project/arbtt-chart/)
![License badge](https://img.shields.io/github/license/liskin/arbtt-chart)

## Overview

arbtt-chart is a …

<!-- FIXME: example image -->

## Installation

Using [pipx][]:

```
pipx ensurepath
pipx install arbtt-chart
```

To keep a local git clone around:

```
git clone https://github.com/liskin/arbtt-chart
make -C arbtt-chart pipx
```

Alternatively, if you don't need the isolated virtualenv that [pipx][]
provides, feel free to just:

```
pip install arbtt-chart
```

[pipx]: https://github.com/pypa/pipx

## Usage

<!-- include tests/readme/help.md -->
    $ arbtt-chart --help
    Usage: arbtt-chart [OPTIONS]
    
    Options:
      --config FILE    Read configuration from FILE.  [default:
                       /home/user/.config/arbtt_chart/config.yaml]
      --config-sample  Show sample configuration file
      --help           Show this message and exit.
<!-- end include tests/readme/help.md -->

<!-- FIXME: example -->

### Configuration file

Secrets (and other options) can be set permanently in a config file,
which is located at `~/.config/arbtt_chart/config.yaml` by default
(on Linux; on other platforms see output of `--help`).

Sample config file can be generated using the `--config-sample` flag:

<!-- include tests/readme/config-sample.md -->
    $ arbtt-chart --config-sample
<!-- end include tests/readme/config-sample.md -->

## Contributing

### Code

We welcome bug fixes, (reasonable) new features, documentation improvements,
and more. Submit these as GitHub pull requests. Use GitHub issues to report
bugs and discuss non-trivial code improvements; alternatively, get in touch
via [IRC/Matrix/Fediverse](https://work.lisk.in/contact/).

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details about the code base
(including running tests locally).

Note that this project was born out of a desire to solve a problem I was
facing. While I'm excited to share it with the world, keep in mind that I'll
be prioritizing features and bug fixes that align with my personal use cases.
There may be times when I'm busy with other commitments and replies to
contributions might be delayed, or even occasionally missed. Progress may come
in bursts. Adjust your expectations accordingly.

### Donations (♥ = €)

If you like this tool and wish to support its development and maintenance,
please consider [a small donation](https://www.paypal.me/lisknisi/10EUR) or
[recurrent support through GitHub Sponsors](https://github.com/sponsors/liskin).

By donating, you'll also support the development of my other projects. You
might like these:

* <!-- FIXME: [name](link) --> – <!-- FIXME: description -->
