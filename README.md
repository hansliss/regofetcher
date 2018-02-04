# regofetcher
Scripts to fetch data from IVT REGO2000, Bosch ProControl and Buderus Gateway Logamatic KM200
and other equipment based on similar network modules.

The shell script getVals.sh uses the Python script to fetch individual values according to
the list in vars.txt, and add an entry to a logfile on CSV format. A new logfile will be
created each month. The script also generates a plot of some of the values, using gnuplot.
You will want to play around a bit with this.

checkRegoNotifications.sh retrieves any notifications and sends email reminders when there are
new ones, or every day for static ones.

Both of these scripts are meant to be run from cron. Here are example crontab entries that will
run both scripts in /home/pi/rego every ten minutes:
    */10 * * * * /home/pi/rego/getVals.sh
    */10 * * * * /home/pi/rego/checkRegoNotifications.sh

Copy config.ini.template to config.ini and edit it, adding the information for your particular
gateway module. Depending on the vendor, you may have to find the correct vendor key, which is
commonly called a "salt", even thought it isn't a salt. Encode the vendor key with Base64.

This is just a quick hack for now (and no, I haven't use Python before, and I'm not a fan),
and may be improved over time.

It's also possible to change some settings using the same technique, presumably by encrypting
input data using the same algorithm, and then using PUT to send it to the gateway. I have not
tried this.

Examples of paths to try are in URLs.txt.
Some examples of parameter formats for "/recordings":
?interval=2018-01-31
?interval=2018-W5
?interval=2018-01




