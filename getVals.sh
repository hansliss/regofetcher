#!/bin/sh

RUNDIR=.
LOGFILE=$RUNDIR/regoVals_`date +"%Y-%m"`.csv

if [ ! -f "$LOGFILE" ]; then
   cat $RUNDIR/vars.txt | sed 's/:/ /' | while read var path; do
       echo -n "$var,"
   done | sed 's/,$//' > $LOGFILE
   echo >> $LOGFILE
fi

cat $RUNDIR/vars.txt | sed 's/:/ /' | while read var path; do
    echo -n `python3 $RUNDIR/getRegoData.py -c $RUNDIR/config.ini -s myrego -p $path -m value`,
done | sed 's/,$//' >> $LOGFILE
echo >> $LOGFILE

