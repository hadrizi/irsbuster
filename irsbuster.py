"""
Usage:
    irsbuster.py stats (-n | --name) <name>
    irsbuster.py download [(-n | --name) <name>] [(-r | --range) <range>]

    Simple IRS buster.
    Order of arguments is important.

    irsbuster has two modes - stats and download.
    stats:
        Fetches data for form %NAME% and saves result to data/result.json.
        You can pass multiple form names e.g., irsbuster.py stats -n "Form-1, Form 2, Form_3"
    
    download:
        Downloads all form %NAME% PDFs within given RANGE(string in format 'xxxx-yyyy')
        and saves them to data/%NAME%/ directory.

Arguments:
    <name>   Product Number of the form. If it contains spaces, then it must be enclosed in quotes(e.g., "Form W-2")
    <range>  Year range, string in format 'xxxx-yyyy' where xxxx is less than yyyy
 
Examples:
    irsbuster.py stats --name "Form W-2"
    irsbuster.py stats --name "Form W-2, Form W-2VI, Form W-2CA, Publ 1"
    irsbuster.py stats --name "Form W-2,Form W-2VI,Form W-2CA,Publ 1"
    irsbuster.py stats --name "Form W-2","Form W-2VI","Form W-2CA","Publ 1"
    irsbuster.py download --name "Form W-2" --range 2002-2013
"""
from pathlib import Path

from docopt import docopt
from src.irsparser import Parser

arguments = docopt(__doc__, help=True)

def sanitize_date_range(date_range_raw):
    date_range_raw = date_range_raw.strip().split('-')
    date_range_raw = [x for x in date_range_raw if x != ""]
    if not date_range_raw or len(date_range_raw) != 2 or (int(date_range_raw[0]) > int(date_range_raw[1])):
        print(f"[!] Range was not valid. Passed {arguments.get('<range>')}. Should be `xxxx-yyyy`, where xxxx is less than yyyy.")
        exit()
    date_range = list(range(int(date_range_raw[0]), int(date_range_raw[1]) + 1))
    return date_range

if arguments['stats']:
    forms = arguments.get("<name>").split(",")
    for form in forms:
        p = Parser(form.strip())
        p.parse()
    if p.results:
        p.dump_json()
        path = Path("data/")
        path.mkdir(parents=True, exist_ok=True)
        with open("data/result.json", "w") as f:
            f.write(p.json_result)
        print("[+] Result in JSON format(additioanlly saved to data/result.json)")
        print(p.json_result)
elif arguments['download']:
    date_range = sanitize_date_range(arguments.get("<range>"))
    forms = arguments.get("<name>").split(",")
    for form in forms:
        p = Parser(form.strip())
        p.download(date_range)
