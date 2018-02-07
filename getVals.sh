#!/bin/sh

CONFFILE=$1
SECTION=$2

RUNDIR=`sed -n '/^\['"$SECTION"'\]/,/^\[/p' $CONFFILE | grep -i "^[ 	]*rundir" | cut -d: -f2 | sed 's/^[ 	]*\(.*\)[ 	]*$/\1/'`

PERIOD=`date +"%Y-%m"`
LOGFILE=$RUNDIR/regoVals_$PERIOD.csv

if [ ! -f "$LOGFILE" ]; then
   cat $RUNDIR/vars.txt | sed 's/:/ /' | while read var path; do
       echo -n "$var,"
   done | sed 's/,$//' > $LOGFILE
   echo >> $LOGFILE
fi

cat $RUNDIR/vars.txt | sed 's/:/ /' | while read var path; do
    echo -n `python3 $RUNDIR/getRegoData.py -c $CONFFILE -s $SECTION -p $path -m value`,
done | sed 's/,$//' >> $LOGFILE
echo >> $LOGFILE

sed 's/#PERIOD#/'"$PERIOD"'/g' $RUNDIR/plot.gpl.tpl | sed 's@#PATH#@'"$RUNDIR"'@g' > $RUNDIR/plot.gpl
gnuplot $RUNDIR/plot.gpl
