from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
from urllib.parse import urljoin
import datetime
from pathlib import Path
import re

"""
Site link removed for personal reasons. Just grabs image from a site, and using the website's URL patterns, scraps all images from the main page over a specified day range.
"""

class HTMLScraper: #Object for SCRAPER, not the image
    def __init__(self,base_url = "https"):
        self.base_url = base_url
        self.html = None #Raw HTML
        self.soup = None #BS4 object

    def _sanitize_alt(self): #Removes any invalid Windows file characters from the filename.
        return re.sub(r'[\\/*?:"<>|]', "", self._grab_alt())

    def _ensure_parsed(self):
        if self.soup is None:
            raise RuntimeError("HTML not parsed. Call load_page() and parse_html() first.")


    def load_page(self): #Parses HTML from given URL
        try:
            html_response = urlopen(self.base_url)
        except Exception as e:
            print(f"Failed to load page: {e}")
            return

        self.html = html_response.read().decode("utf-8")

    def parse_html(self):
        if not self.html:
            print(f"No valid HTML.")
            return
        try:
            self.soup = BeautifulSoup(self.html, "lxml")
        except Exception as e:
            print(f"Failed to parse HTML: {e}")
            return

    def _grab_src(self):
        self._ensure_parsed()
        for tag in self.soup.find_all("img"):
            src_attribute = tag.get("src")
            if src_attribute and "comics" in src_attribute:
                return src_attribute
        return

    def _grab_alt(self):
        self._ensure_parsed()
        comic_src = self._grab_src()
        for tag in self.soup.find_all("img"):
            if comic_src == tag.get("src"):
                return tag.get("alt")
        return

    def _grab_publish_date_str(self):
        self._ensure_parsed()
        return self._grab_src().split("/")[-1].split(".")[0]

    def _grab_publish_date_datetime(self):
        self._ensure_parsed()
        return datetime.datetime.strptime(self._grab_publish_date_str(), "%Y-%m-%d").date()

    def _grab_file_type(self):
        self._ensure_parsed()
        return self._grab_src().split(".")[-1]

    def _make_file_name(self):
        self._ensure_parsed()
        return f"{self._grab_publish_date_str()}-{self._sanitize_alt() or 'comic'}.{self._grab_file_type()}"

    def _make_full_url(self):
        self._ensure_parsed()
        return urljoin(self.base_url, self._grab_src())

    def scrape_comic(self):
        self._ensure_parsed()
        file_name = self._make_file_name()
        if not Path(file_name).exists():
            with urlopen (self._make_full_url()) as response:
                image_data = response.read()

            with open(file_name, "wb") as saved_comic:
                saved_comic.write(image_data)
            print(f"{file_name} saved.")

        else:
            print(f"{file_name} already exists in the directory")

    def output_testing(self):
        return(
                  f"Alttext: {self._grab_alt()}\n"
                  f"src attribute: {self._grab_src()}\n"
                  f"filetype: {self._make_file_name()}\n"
                  f"Publish date: {self._grab_publish_date_str()}\n"
                  f"Full url: {self._make_full_url()}\n"
        )


sinfest = HTMLScraper()
sinfest.load_page()
sinfest.parse_html()
sinfest.scrape_comic() # Gives issue if there's pnctuation i filename
print(sinfest.output_testing())

def get_day_difference(day_difference=0):
    todays_date = datetime.datetime.now().date()
    delta = datetime.timedelta(days=(day_difference))
    nth_date = (todays_date)-(delta)
    return nth_date.strftime("%Y-%m-%d")



#TESTING VARIABLES

for i in range(15):

    date_str = get_day_difference(i)
    dynamic_link = f"https:/view.php?date={date_str}"
    sinfest = HTMLScraper(base_url=dynamic_link)
    sinfest.load_page()
    sinfest.parse_html()
    sinfest.scrape_comic()


