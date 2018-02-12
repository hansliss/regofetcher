#!/bin/sh

CONFFILE=$1
SECTION=$2

RUNDIR=`sed -n '/^\['"$SECTION"'\]/,/^\[/p' $CONFFILE | grep -i "^[ 	]*rundir" | cut -d: -f2 | sed 's/^[ 	]*\(.*\)[ 	]*$/\1/'`
MAILRCPT=`sed -n '/^\['"$SECTION"'\]/,/^\[/p' $CONFFILE | grep -i "^[ 	]*mailrcpt" | cut -d: -f2 | sed 's/^[ 	]*\(.*\)[ 	]*$/\1/'`

find $RUNDIR -maxdepth 1 -name notifications_save.txt -mtime +1 -exec rm {} \;

if [ ! -f $RUNDIR/notifications_save.txt ]; then
    touch $RUNDIR/notifications_save.txt
fi

python3 $RUNDIR/getRegoData.py -c $CONFFILE -s $SECTION -p /notifications -m errcodes > $RUNDIR/notifications_new.txt

if diff >/dev/null 2>&1 $RUNDIR/notifications_save.txt $RUNDIR/notifications_new.txt; then
    rm $RUNDIR/notifications_new.txt
else
    mail -s "Notifications from heat pump" -a "Content-Type: text/html; charset: UTF-8" $MAILRCPT < $RUNDIR/notifications_new.txt
    mv $RUNDIR/notifications_new.txt $RUNDIR/notifications_save.txt
fi
    
