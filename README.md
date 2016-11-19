# Open Pension Scraper

[![Build Status][travis-image]][travis-url]

This repo contains tools and [meta]data for the purpose of extracting publicly-available
online information to be used by Open Pension.

Open Pension is a "Hasadna" project, aiming to reveal the secrets behind the Israeli pension market.

## Pre Requirements

<<<<<<< HEAD
* Make sure you have Python 3.x and pip installed.

## Installation

Not yet.

## Tests

Not yet.
=======
* Make sure you have Python `3.x` and `virtualenv` installed.
* For batch-dumping, you'll also need a [redis](http://redis.io/) server.

## Installation

* `virtualenv -p python3 venv`
* `./envrun.sh pip install -r requirements.txt`

**Note:** if you `source venv/bin/activate` in a shell,
you can skip the `./envrun.sh` in commands here
(still, it's handy if you open a shell only to run `rq worker`).

If you want `rq-dashboard` (for monitoring batch jobs via browser):

* `./envrun.sh pip install rq-dashboard`

## Running

### Dump portfolio of a single month

[this is something you don't need redis for]

For exmaple: `./envrun.sh python web-sources/gemelnet.py 101 2016 1`
would write Jan 2016 portfolio of kupa 101 to `data/101-2016-01.csv`.

### Batch dump portfolios over a period

run these on separate shells:

* [If you don't have a running redis server] `redis-server`

* `./envrun.sh rq worker`

Exmaple query: `./envrun.sh python batch_gemelnet.py 101 1999 8 2002 4`
would dump all months between Aug 1999 and April 2002 (into separate files).

Monitoring jobs:

* From console: `./envrun.sh rq info`
* via browser: `./envrun.sh rq-dashboard`

## Tests

Only pep8 so far ;)
>>>>>>> 46a98734a46b386740e3b2ad7c7433b0f53c3db7

## Contribute

Just fork and do a pull request (;

[travis-image]: https://api.travis-ci.org/hasadna/open-pension-net-scraper.svg?branch=master
[travis-url]: https://travis-ci.org/hasadna/open-pension-net-scraper
