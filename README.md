### Netgear-AirCard

A script to check the status of a Netgear AirCard router with Python3.

CLI Usage:

    ./ac.py -h
    
    usage: ac.py [-h] [--ip IP] [--password PASSWORD] [--no-login] [--debug]
    
    Script to check the status of a Netgear AirCard router.
    
    optional arguments:
      -h, --help            show this help message and exit
      --ip IP               IP Address of the AirCard
      --password PASSWORD, -p PASSWORD
                            Admin Password.
      --no-login, -n        Don't log in to the router

#### Requirements

* requests
* BeautifulSoup4

