import sys
import os
import csv
import xml.etree.ElementTree as XML
import requests
import argparse
import codecs

API_URL = 'http://gemelnet.mof.gov.il/tsuot/ui/tsuotHodXML.aspx'
OUTPUT_DIR = 'data'


def _parse_xml(xml):
    "Convert Gemelnet XML result to array of dict per <Row/>"
    return [
        dict([(field.tag, field.text) for field in row])
        for row in xml.iter('Row')]


def _load_xml_monthly_portfolio(kupa_id, year, month):
    "Query Gemelnet for a kupa's monthly portfolio. Returns XML node."
    period = '{:04d}{:02d}'.format(year, month)
    req = requests.get(API_URL, params={
        'dochot': 1, 'sug': 4,
        'miTkfDivuach': period,
        'adTkfDivuach': period,
        'kupot': kupa_id
        })
    req.encoding = 'UTF-8'  # Gemelnet doesn't declare UTF-8 at header.
    return XML.fromstring(req.text)


def save_csv_monthly_portfolio(kupa_id, year, month):
    """Query Gemelnet for a kupa's monthly portfolio and save as a CSV file.
Rerurns file path."""
    xml = _load_xml_monthly_portfolio(kupa_id, year, month)
    result = _parse_xml(xml)
    filepath = os.path.join(
        OUTPUT_DIR,
        '{}-{:04d}-{:02d}.csv'.format(kupa_id, year, month))
    outfile = open(filepath, 'w')
    outfile.write(str(codecs.BOM_UTF8, 'utf-8'))  # Help Windows detects UTF-8.
    sheet = csv.writer(outfile)
    sheet.writerow(['קופה', 'תקופה', 'קוד', 'נכס', 'כמות'])
    pretty_month = '{:02d}/{:04d}'.format(month, year)
    for r in result:
        sheet.writerow([
            kupa_id, pretty_month,
            r['ID_NATUN'], r['SHM_NATUN'], r['ERECH_NATUN']])
    return filepath


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("kupa", type=int, help="numeric code of kupa")
    parser.add_argument("year", type=int)
    parser.add_argument("month", type=int)
    args = parser.parse_args()
    print('downloading...')
    print('saved {}.'.format(
        save_csv_monthly_portfolio(args.kupa, args.year, args.month)))
