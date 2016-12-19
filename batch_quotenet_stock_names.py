import sys
import re
import requests
import time
import codecs
import csv


BOM = str(codecs.BOM_UTF8, 'utf-8')
pat = re.compile(r'Array\("([^"]*)", "Stocks", "[^\|]*\|([^\|]*)\|')
QUERY_TEMPLATE = (
    'http://www.quotenet.com/ajax/SearchController_Suggest?max_results=25&'
    'Keywords_mode=APPROX&Keywords=&query={}&bias=100&target_id=0')


def search_quotenet_stocks(q):
    "query quotenet's search field autocomplete for stocks"
    response = requests.get(QUERY_TEMPLATE.format(q))
    return pat.findall(response.text)


if __name__ == '__main__':
    outfile = sys.stdout
    outfile.write(BOM)
    csv = csv.writer(outfile)
    for q in sys.stdin.readlines():
        q = q.strip()
        sys.stderr.write(q+'\n')
        rows = search_quotenet_stocks(q)
        if rows:
            for r in rows:
                csv.writerow([q]+list(r))
        else:
            csv.writerow([q, 'Not found', '-'])
