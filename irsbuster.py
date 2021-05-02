import sys

from pathlib import Path

from src.cli import CLI
from src.irsparser import Parser

USAGE = '''
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
'''

args = CLI.parse(" ".join(sys.argv[1:]))

if not args:
    raise SystemExit(USAGE)

if args.get("HELP"):
    print(USAGE)
    exit()
elif args.get("STATS"):
    p = Parser(args.get("STAT_NAME"))
    p.parse()
    path = Path("data/")
    path.mkdir(parents=True, exist_ok=True)
    with open("data/result.json", "w") as f:
        f.write(p.json_result)
    print("[+] Result in JSON format(additioanlly saved to data/result.json)")
    print(p.json_result)
elif args.get("DOWNLOAD"):
    date_range_raw = args.get("RANGE").strip().split('-')
    # sanitize raw range raw list
    date_range_raw = [x for x in date_range_raw if x != ""]
    if not date_range_raw or len(date_range_raw) != 2 or (int(date_range_raw[0]) > int(date_range_raw[1])):
        print(f"[!] Range was not valid. Passed {args.get('RANGE')}. Should be `xxxx-yyyy`, where xxxx is less than yyyy.")
        exit()
    date_range = list(range(int(date_range_raw[0]), int(date_range_raw[1]) + 1))
    p = Parser(args.get("DOWNLOAD_NAME"))
    p.download(date_range)
else:
    raise SystemExit(USAGE)