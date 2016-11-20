# Open Pension Scraper

[![Build Status][travis-image]][travis-url]

This repo contains tools and [meta]data for the purpose of extracting publicly-available
online information to be used by Open Pension.

Open Pension is a "Hasadna" project, aiming to reveal the secrets behind the Israeli pension market.

## Pre Requirements

* Make sure you have Python `3.x` and `virtualenv` installed.

## Installation
```shell
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running

**Note:** remember to `source venv/bin/activate` on each new shell.

### Dump portfolio of a single month

For exmaple: `python web-sources/gemelnet.py 101 2016 1`
would write Jan 2016 portfolio of kupa 101 to `data/101-2016-01.csv`.

## Tests

Not yet.

## Contribute

Just fork and do a pull request (;

[travis-image]: https://api.travis-ci.org/hasadna/open-pension-net-scraper.svg?branch=master
[travis-url]: https://travis-ci.org/hasadna/open-pension-net-scraper
