from glob import glob
from decimal import Decimal, InvalidOperation
import os
import csv
import codecs
import argparse


def compute_totals(year, month):
    result = []
    for filename in sorted(glob('data/*-{:04}-{:02}.csv'.format(year, month))):
        kupa = os.path.basename(filename).split('-')[0]
        if not kupa[0].isdigit():
            continue  # totals, performance, etc.
        total = Decimal(0)
        for i, r in enumerate(csv.reader(open(filename))):
            if not i:
                continue  # Skip header line
            try:
                total += Decimal(r[4])
            except InvalidOperation:
                pass
        result.append([kupa, '{:.2f}'.format(total)])
    outfilepath = 'data/totals-{:04d}-{:02d}.csv'.format(year, month)
    outfile = open(outfilepath, 'w')
    outfile.write(str(codecs.BOM_UTF8, 'utf-8'))  # Help Windows detect UTF-8.
    sheet = csv.writer(outfile)
    sheet.writerow(['קופה', 'אחזקות - {:02}-{:04}'.format(month, year)])
    for r in sorted(result, key=lambda x: int(x[0])):
        sheet.writerow(r)
    return outfilepath


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int)
    parser.add_argument("month", type=int)
    args = parser.parse_args()
    print('saved {}'.format(
        compute_totals(args.year, args.month)))
