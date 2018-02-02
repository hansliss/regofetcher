# regofetcher
Scripts to fetch data from IVT REGO2000, Bosch ProControl and Buderus Gateway Logamatic KM200

The shell script will use the Python script to fetch individual values according to the list
in vars.txt, and add an entry to a logfile on CSV format. A new logfile will be created each
month.

Edit the config file, adding the information for your particular gateway module. You will have
to search for the vendor key, which is typically called a "salt", even thought it isn't a salt.
Encode the vendor key with Base64.

This is just a quick hack for now, and may be improved over time. An obvious addition is support
for retrieving notifications (path: "/notifications") and sending email reminders when there
are active notifications.

It's also possible to change some setting using the same technique, presumably by encrypting
input data using the same algorithm, and then using PUT to send it to the gateway. I have not
tried this.

Examples of paths to try are in URLs.txt.
Some examples of parameter formats for "/recordings":
?interval=2018-01-31
?interval=2018-W5
?interval=2018-01
