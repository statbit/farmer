
# Crontab setup

The best way to set this up is to set the script up as a crontab
that is run on the Pi:

```
0 1 * * * /home/pi/git/farmer/run.sh
@reboot /home/pi/git/farmer/run.sh
```
