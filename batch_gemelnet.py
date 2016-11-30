import argparse
from redis import Redis
from rq import Queue
from web_sources.gemelnet import save_csv_monthly_portfolio


def get_timeline(kupa, from_year, from_month, to_year, to_month):
    "Queue (as rq jobs) portfolio CSV dump of kupa for all months in range."
    year = args.from_year
    month = args.from_month
    q = Queue(connection=Redis())
    while year < args.to_year or year == args.to_year and month < args.to_month:
            q.enqueue(save_csv_monthly_portfolio, args=(args.kupa, year, month))
            if month < 12:
                month += 1
            else:
                year += 1
                month = 1
    return len(q)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("kupa", type=int, help="numeric code of kupa")
    parser.add_argument("from_year", type=int)
    parser.add_argument("from_month", type=int)
    parser.add_argument("to_year", type=int)
    parser.add_argument("to_month", type=int)
    args = parser.parse_args()
    print("{} jobs in queue".format(
        get_timeline(
            args.kupa, args.from_year, args.from_month,
            args.to_year, args.to_month)))
