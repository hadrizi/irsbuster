# Description
Simple IRS buster

# Dependencies
- python 3.5+
- requests 2.25.1
- beautifulsoup4 4.9.4

# Installation
All dependencies can be installed using `make`:
1. Go to root directory of the project
2. Run `make init`

If you don't have `make` installed, run `pip install -r requirements.txt` instead

# Usage
```
Simple IRS buster

Usage:
    python irsbuster.py --help
    python irsbuster.py stats [-n NAME]
    python irsbuster.py download [-n NAME] [-r RANGE]

    Order of arguments is important

    irsbuster has two modes - stats and download
    stats:
        Fetches data for form %NAME% and saves result to data/result.json
    
    download:
        Downloads all form %NAME% PDFs within given RANGE(string in format 'xxxx-yyyy')
        and saves them to data/%NAME%/ directory.
```