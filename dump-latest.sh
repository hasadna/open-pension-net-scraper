#!/bin/bash
cd "$(dirname "$0")"
if [ -z "$1" ] ; then
	MONTHS_AGO=2 # 2 is safe. Last month isn't available early in the month
else
	MONTHS_AGO="$1"
fi
# performance reports should be >=12 months
MONTHS_AGO_P=$(echo "11+$MONTHS_AGO"|bc)
source "venv/bin/activate"
Y=$(date --date "$MONTHS_AGO months ago" +%4Y)
M=$(date --date "$MONTHS_AGO months ago" +%2m)
Yp=$(date --date "$MONTHS_AGO_P months ago" +%4Y)
Mp=$(date --date "$MONTHS_AGO_P months ago" +%2m)
for k in $(sed -e 's/,.*//' -e 's/^[^0-9]//' < metadata/kupot.csv) ; do
	echo $k
	python batch_gemelnet.py $k $Y $M $Y $M
	python batch_gemelnet.py $k $Yp $Mp $Y $M -t p
done
