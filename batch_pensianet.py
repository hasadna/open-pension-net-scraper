import argparse
from redis import Redis
from rq import Queue
from web_sources.pensianet import (
    save_csv_monthly_portfolios, save_csv_performance)


def get_asset_timeline(from_year, from_month, to_year, to_month):
    "Queue (as rq jobs) CSV dump of all portfolios for each month in range."
    year = args.from_year
    month = args.from_month
    q = Queue(connection=Redis())
    while year < args.to_year or year == args.to_year and month <= args.to_month:
            q.enqueue(save_csv_monthly_portfolios, args=(year, month))
            if month < 12:
                month += 1
            else:
                year += 1
                month = 1
    return len(q)


def get_performance(from_year, from_month, to_year, to_month):
    "Queue (as a single rq job) CSV dump performance of all kranot for month range."
    q = Queue(connection=Redis())
    q.enqueue(save_csv_performance, args=(
        args.from_year, args.from_month,
        args.to_year, args.to_month))
    return len(q)


OPERATIONS = {'a': get_asset_timeline, 'p': get_performance}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("from_year", type=int)
    parser.add_argument("from_month", type=int)
    parser.add_argument("to_year", type=int)
    parser.add_argument("to_month", type=int)
    parser.add_argument(
        "--type", "-t", choices=['a', 'p'], default='a',
        help="Report type: assets [default] or performance")
    args = parser.parse_args()
    print("{} jobs in queue".format(
        OPERATIONS[args.type](
            args.from_year, args.from_month,
            args.to_year, args.to_month)))
