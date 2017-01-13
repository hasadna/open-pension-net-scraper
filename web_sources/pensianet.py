import sys
import os
import csv
import json
import xml.etree.ElementTree as XML
import calendar
import requests
import argparse
import codecs
import paths

API_URL = 'http://pensyanet.cma.gov.il/Parameters/ExportToXML'

# API accepts a single param, vm, containing a JSON structure
# Functions should use API_VM_TEMPLATE.copy() and replace all
# "???" values
API_VM_TEMPLATE = {
    "XmlExportVM": {
        "SelectedMainReportType": 1,
        "SelectedReportType": "???"
    },
    "IsCustomReportDates": True,
    "IsCustomReportDatesReversed": False,
    "MaxReportDate": "???",
    "MinReportStartDate": "1998-12-31T22:00:00.000Z",
    "ReportStartDate": "???",
    "ReportEndDate": "???",
    "IsUserInternal": False,
    "ParametersTab": 0,
    "LastParametersTab": 0,
    "ShowInvestements": True,
    "ShowInvestementsSwitch": False,
    "ShowMergesSwitch": False,
    "ShowMerges": True,
    "ShowOpenCloseAllSwitch": False,
    "OpenAll": False,
    "guid": 318
}

API_REPORT_TYPE_PERFORMANCE = "3"
API_REPORT_TYPE_PORTFOLIO = "4"


def _pensianet_month_format(year, month):
    "Pensianet seems to be using 22:00 of last day in month for params"
    return "{:04d}-{:02d}-{:02d}T22:00:00.000Z".format(
            year, month,
            calendar.monthrange(year, month)[1])


def _parse_xml(xml):
    "Convert Pensianet XML result to array of dict per <ROW/>"
    return [
        dict([(field.tag, field.text) for field in row])
        for row in xml.iter('ROW')]


def _load_xml_monthly_portfolios(year, month):
    "Query Pensianet for monthly portfolio of all kranot. Returns XML node."
    vm = API_VM_TEMPLATE.copy()
    vm['XmlExportVM']['SelectedReportType'] = API_REPORT_TYPE_PORTFOLIO
    formatted_month = _pensianet_month_format(year, month)
    vm['MaxReportDate'] = formatted_month
    vm['ReportStartDate'] = formatted_month
    vm['ReportEndDate'] = formatted_month
    req = requests.post(API_URL, data={'vm': json.dumps(vm)})
    req.encoding = 'UTF-8'  # Pensianet doesn't declare UTF-8 at header.
    return XML.fromstring(req.text)


def _load_xml_performance(from_year, from_month, to_year, to_month):
    "Query Pensianet for performance over a period"
    # decrease month (for some reason, API skips from_month)
    if from_month == 1:
        from_month = 12
        from_year -= 1
    else:
        from_month -= 1
    vm = API_VM_TEMPLATE.copy()
    vm['XmlExportVM']['SelectedReportType'] = API_REPORT_TYPE_PERFORMANCE
    formatted_from = _pensianet_month_format(from_year, from_month)
    formatted_to = _pensianet_month_format(to_year, to_month)
    vm['MaxReportDate'] = formatted_to
    vm['ReportStartDate'] = formatted_from
    vm['ReportEndDate'] = formatted_to
    req = requests.post(API_URL, data={'vm': json.dumps(vm)})
    req.encoding = 'UTF-8'  # Pensianet doesn't declare UTF-8 at header.
    return XML.fromstring(req.text)


def save_csv_monthly_portfolios(year, month):
    """Query Pensianet for monthly portfolios of all kranot, and save as a CSV file.
Rerurns file path."""
    xml = _load_xml_monthly_portfolios(year, month)
    result = _parse_xml(xml)
    filepath = os.path.join(
        paths.PENSIANET_PATH,
        '{:04d}-{:02d}.csv'.format(year, month))
    outfile = open(filepath, 'w')
    outfile.write(str(codecs.BOM_UTF8, 'utf-8'))  # Help Windows detects UTF-8.
    sheet = csv.writer(outfile)
    sheet.writerow(['תקופה', 'קוד קרן', 'שם קרן', 'קוד נכס', 'תאור נכס', 'כמות'])
    pretty_month = '{:02d}/{:04d}'.format(month, year)
    for r in result:
        sheet.writerow([
            pretty_month, r['ID_KRN'], r['SHM_KRN'],
            r['ID_NATUN'], r['SHM_NATUN'], r['ERECH_NATUN']])
    return filepath


def save_csv_performance(
        from_year, from_month, to_year, to_month):
    """Query Pensianet for performance and save as a CSV file.
Rerurns file path."""
    xml = _load_xml_performance(
        from_year, from_month, to_year, to_month)
    result = _parse_xml(xml)
    filepath = os.path.join(
        paths.PENSIANET_PATH,
        'perf-{:04d}-{:02d}-{:04d}-{:02d}.csv'.format(
            from_year, from_month, to_year, to_month))
    outfile = open(filepath, 'w')
    outfile.write(str(codecs.BOM_UTF8, 'utf-8'))  # Help Windows detects UTF-8.
    sheet = csv.writer(outfile)
    sheet.writerow([
        'קרן', 'שם', 'תקופה', 'יתרת נכסים בפועל', 'תשואה נומינלית בפועל',
        'תשואה נומינלית השקעות חופשיות', 'תשואה דמוגרפית',
        'תשואה נומינלית עם דמוגרפית', 'עודף/גירעון אקטוארי רבעוני'])
    for r in result:
        sheet.writerow([
            r['ID_KRN'], r['SHM_KRN'], '{}/{}'.format(
                r['TKF_DIVUACH'][4:], r['TKF_DIVUACH'][:4]),
            r.get('YIT_NCHASIM_BFOAL', ''), r.get('TSUA_NOMINALI_BFOAL', ''),
            r.get('TSUA_NOM_HASHKAOT_HOFSHIOT', ''), r.get('TSUA_DEMOGRAPHIT', ''),
            r.get('TSUA_NOMINALI_IM_DEMOGRAPHIT', ''),
            r.get('ODEF_GIRAON_ACTUARI_RIVONI', '')])
    return filepath


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("year", type=int)
    parser.add_argument("month", type=int)
    parser.add_argument(
        "--type", "-t", choices=['a', 'p'], default='a',
        help="Report type: assets [default] or performance")
    args = parser.parse_args()
    print('downloading...')
    if args.type == 'a':
        print('saved {}.'.format(
            save_csv_monthly_portfolios(args.year, args.month)))
    else:
        if args.month == 12:
            from_year, from_month = args.year, 1
        else:
            from_year, from_month = args.year-1, args.month+1
        print('saved {}.'.format(
            save_csv_performance(
                from_year, from_month, args.year, args.month)))
