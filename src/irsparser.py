import requests
import json
import os

from bs4 import BeautifulSoup

from urllib.parse import urlunsplit, urlencode

class Parser:
    url_scheme = "https"
    url_path = "/app/picklist/list/priorFormPublication.html"
    netloc = "apps.irs.gov"

    # for more info about url parameters see
    # https://www.irs.gov/help/find-help
    # and
    # https://www.irs.gov/forms-pubs/features-of-the-file-listings-application
    url_params = {
        "resultsPerPage": 200,
        "sortColumn": "sortOrder",
        "indexOfFirstRow": 0,
        "criteria": "formNumber",
        "formNumber": "false",
        "isDescending": "false"
    }

    results = []
    links = {}
    json_result = ""

    def __init__(self, form_name: str, *args, **kwargs):
        self.url_params["value"] = form_name
        self.form_name = self.url_params["value"]
        self.url = self._build_url()

    def parse(self):
        print(f"[~] Looking for {self.form_name}")

        html_dict = self._get_page_dict()
        pages_count = self._count_pages(html_dict)

        print(f"[+] HTML page retrieved, there are {pages_count} pages of raw data(each page contains {self.url_params['resultsPerPage']} entries)")
        print(f"[!] It is not guaranteed that there is the exact form you desire(since IRS app searches for names LIKE you passed, not exact)")

        print(f"[~] Retrieving form data")

        years = []
        title = ""

        for i in range(0, pages_count):
            # emulating pagination(each page starts with last index of previous page)
            self.url_params["indexOfFirstRow"] = self.url_params["resultsPerPage"] * i
            self.url = self._build_url()
            html_dict = self._get_page_dict()
            # divs with `odd` and `even` class names contains useful data(forms data) so we fetch them
            forms = html_dict.find_all(True, class_=["odd", "even"])
            
            for form in forms:
                if form.find("td", class_="LeftCellSpacer").text.strip() == self.form_name:
                    if not title:
                        title = form.find("td", class_="MiddleCellSpacer").text.strip()
                    years.append(int(form.find('td', class_="EndCellSpacer").text))
                    self.links[int(form.find('td', class_="EndCellSpacer").text)] = form.find("a", href=True)['href']

        if not years and not title:
            print("[!] Desired form was not found")
            exit()
        self.results.append(self._build_form_data(title, years))
        print(f"[+] Form data retrieved")
        self.json_result = json.dumps(self.results, indent=4, sort_keys=True)

    def download(self, years):
        self.parse()
        print(f"[~] Downloading PDFs for form {self.form_name} within range {min(years)}-{max(years)} to data/{self.form_name}/")

        try:
            os.mkdir(f"data/{self.form_name}/")
        except FileExistsError:
            pass
        
        count = 0
        for year in years:
            if year in self.links.keys():
                f = requests.get(self.links[year], allow_redirects=True)
                open(f"data/{self.form_name}/{self.form_name} - {year}.pdf", "wb").write(f.content)
                count += 1
        if count:
            print(f"[+] {count} PDFs were saved to data/{self.form_name}/")
            if(len(years) - count > 0):
               print(f"[+] {len(years) - count} PDFs were not found. Probably because there are no entries for these years.") 
        else:
            print(f"[!] There was no PDFs within given range")

    def _build_form_data(self, title: str, years: list[int]) -> dict:
        return {
            "form_number": self.form_name,
            "form_title": title,
            "min_year": min(years),
            "max_year": max(years)
        }

    def _get_page_dict(self) -> BeautifulSoup:
        page = requests.get(self.url)
        return BeautifulSoup(page.content, 'html.parser')
    
    def _count_pages(self, html_dict: BeautifulSoup) -> int:
        pagination_bottom = html_dict.find_all(True, class_="paginationBottom")
        '''
        We count all 'a' tags from paginationBottom 'div'.
        One may ask why we don't add 1 for the page we already on,
        since the paginationBottom div looks like this
            <div class = "paginationBottom">
                <b>1</b> <-- page we are on
                <a>2</a>
                ...
                <a>n</a>
            </div>
        That is because at the end it has <a>Next</a> tag which leads to page next to the one we are on, 
        so this 'Next' tag indemnifies mssing 1.
        (alternatively, we can write `len - 1 + 1` but it seems obscuring to me)

        However, if page count is zero it means that there was only one page of data, so `Next` is not in any tag
        and we should add 1 in that case.
        '''
        if not pagination_bottom:
            print("[!] Desired form was not found")
            exit()
        count = len(pagination_bottom[0].find_all("a"))
        if count == 0:
            count += 1
        return count

    def _build_url(self) -> str:
        if not self.url_params["value"]:
            raise KeyError("Desired form name is not provided")

        params = urlencode(self.url_params)
        return urlunsplit((self.url_scheme, self.netloc, self.url_path, params, ""))
        

