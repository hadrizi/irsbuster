# Description
Simple [IRS](https://apps.irs.gov/app/picklist/list/priorFormPublication.html) buster

# Dependencies
- python 3.5+
- requests 2.25.1
- beautifulsoup4 4.9.4
- docopt 0.6.2

# Installation
All dependencies can be installed using `make`:
1. Go to root directory of the project
2. Run `make init`

If you don't have `make` installed, run `pip install -r requirements.txt` instead

# Usage
```
Usage:
    irsbuster.py stats (-n | --name) <name>
    irsbuster.py download [(-n | --name) <name>] [(-r | --range) <range>]

    Simple IRS buster.
    Order of arguments is important.

    irsbuster has two modes - stats and download.
    stats:
        Fetches data for form <name> and saves result to data/result.json.
        You can pass multiple form names e.g., irsbuster.py stats -n "Form-1, Form 2, Form_3"
    
    download:
        Downloads all form <name> PDFs within given <range>(string in format 'xxxx-yyyy')
        and saves them to data/<name>/ directory.

Arguments:
    <name>   Product Number of the form. If it contains spaces, then it must be enclosed in quotes(e.g., "Form W-2")
    <range>  Year range, string in format 'xxxx-yyyy' where xxxx is less than yyyy
 
Examples:
    irsbuster.py stats --name "Form W-2"
    irsbuster.py stats --name "Form W-2, Form W-2VI, Form W-2CA, Publ 1"
    irsbuster.py stats --name "Form W-2,Form W-2VI,Form W-2CA,Publ 1"
    irsbuster.py download --name "Form W-2" --range 2002-2013
```
