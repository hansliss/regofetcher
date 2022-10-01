#!/bin/sh

CONFFILE=$1
SECTION=$2

RUNDIR=`sed -n '/^\['"$SECTION"'\]/,/^\[/p' $CONFFILE | grep -i "^[ 	]*rundir" | cut -d: -f2 | sed 's/^[ 	]*\(.*\)[ 	]*$/\1/'`
BINDIR=`dirname $0`

PERIOD=`date +"%Y-%m"`
LOGFILE=$RUNDIR/regoVals_$PERIOD.csv

if [ ! -f "$LOGFILE" ]; then
    done=no
    grep "^scalar:" $RUNDIR/URLs.txt | cut -d: -f2,3 | sed 's/:/ /' | while read status path; do
        if [ "$done" = "yes" ]; then
            echo -n ","
        fi
        done=yes
	echo -n "$path"
    done > $LOGFILE
    echo >> $LOGFILE
fi

done=no
grep "^scalar:" $RUNDIR/URLs.txt | cut -d: -f2,3 | sed 's/:/ /' | while read status path; do
    if [ "$done" = "yes" ]; then
	echo -n ","
    fi
    done=yes
    if [ "x$status" = "xon" ]; then
	echo -n `python3 $BINDIR/getRegoData.py -c $CONFFILE -s $SECTION -p $path -m value`
    fi
done >> $LOGFILE
echo >> $LOGFILE

sed 's/#PERIOD#/'"$PERIOD"'/g' $RUNDIR/plot.gpl.tpl | sed 's@#PATH#@'"$RUNDIR"'@g' > $RUNDIR/plot.gpl
gnuplot $RUNDIR/plot.gpl
