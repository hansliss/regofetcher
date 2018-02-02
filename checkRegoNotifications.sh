#!/bin/sh

RUNDIR=.
CONFFILE="$RUNDIR/config.ini"
CONFSECTION="myrego"
MAILRCPT=<youremail@example.com>

find $RUNDIR -maxdepth 1 -name notifications_save.txt -mtime +1 -exec rm {} \;

if [ ! -f $RUNDIR/notifications_save.txt ]; then
    touch $RUNDIR/notifications_save.txt
fi

python3 $RUNDIR/getRegoData.py -c $CONFFILE -s $CONFSECTION -p /notifications -m values > $RUNDIR/notifications_new.txt

if diff $RUNDIR/notifications_save.txt $RUNDIR/notifications_new.txt; then
    rm $RUNDIR/notifications_new.txt
else
    mail -s "Notifications from heat pump" $MAILRCPT < $RUNDIR/notifications_new.txt
    mv $RUNDIR/notifications_new.txt $RUNDIR/notifications_save.txt
fi
    
