# regofetcher
Scripts to fetch data from *IVT REGO2000*, *Bosch ProControl* and *Buderus Gateway Logamatic KM200*
and other equipment based on similar network modules.

NOTE: [FHEM](http://www.fhem.de/) has a module called [KM200](https://wiki.fhem.de/wiki/Buderus_Web_Gateway) that
should be able to talk to all those units. Give it a try, unless you want to use this as a
base for playing around and building your own monitoring tools.

## Setting up
Copy **config.ini.template** to **config.ini** and edit it, adding the information for your particular
gateway module. Depending on the vendor, you may have to find the correct vendor key, which is
commonly called a "salt", even thought it isn't a salt. Encode the vendor key with Base64.

In order to enumerate valid paths to check on your unit, use the "-x" switch to traverse
the tree from one or more starting points, and print out all the recognized leaves. Then
you can check each leaf manually to determine what it represents. Use a command like this
to enumerate the paths:

```bash
python3 getRegoData.py -c config.ini -s myrego -x -p "/,/dhwCircuits,/heatingCircuits,/recordings,/solarCircuits,/system,/gateway,/heatSources,/notifications"
```

Use the output from this to update the file **URLs.txt**, which is used by the shell script
**getVals.sh** to fetch the actual data. To initialize the file, you can use this command:

```bash
python3 getRegoData.py -c config.ini -s myrego -x -p "/,/dhwCircuits,/heatingCircuits,/recordings,/solarCircuits,/system,/gateway,/heatSources,/notifications" | grep "^scalar:" | sed 's/scalar/scalar:on/' > URLs.txt
```

Then change any values you don't need to fetch on every run to "off" in the file.

## Operation
**getVals.sh** uses the Python script to fetch individual values according to the list in **URLs.txt**,
and adds an entry to a logfile on CSV format. All the values listed in URLs.txt will be represented
as columns in the CSV file, but only the ones marked "on" will be fetched from the gateway.

A new logfile will be created each month.
The script also generates a plot of some of the values, using gnuplot.
You will want to play around a bit with this.

**checkRegoNotifications.sh** retrieves any notifications and sends email reminders when there are
new ones, or every day while they are active.

Both of these scripts are meant to be run from cron. Here are example crontab entries that will
run both scripts in /home/pi/rego every ten minutes:
```
*/10 * * * * /home/pi/rego/getVals.sh /home/pi/rego/config.ini myrego
*/10 * * * * /home/pi/rego/checkRegoNotifications.sh /home/pi/rego/config.ini myrego
```

This is just a quick hack for now (and no, I haven't used Python before, and I'm not a fan),
and it may be improved over time.

It's also possible to change some settings using the same technique, presumably by encrypting
input data using the same algorithm, and then using PUT to send it to the gateway. I have not
tried this.

Some examples of parameter formats for "/recordings":
- ?interval=2018-01-31
- ?interval=2018-W5
- ?interval=2018-01


