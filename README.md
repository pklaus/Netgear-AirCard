### Netgear-AirCard

A script to check the status of a Netgear AirCard router with Python3.

CLI Usage:

    ./ac.py -h
    
    usage: ac.py [-h] [--no-login] [--password PASSWORD] [--ip IP]
    
    Script to check the status of a Netgear AirCard router.
    
    optional arguments:
      -h, --help            show this help message and exit
      --no-login, -n        Don't log in to the router
      --password PASSWORD, -p PASSWORD
                            Admin Password.
      --ip IP               IP Address of the AirCard

#### Requirements

* requests
* BeautifulSoup4

