from bs4 import BeautifulSoup
import requests
from feedgen.feed import FeedGenerator
from datetime import datetime
from zoneinfo import ZoneInfo
import re

URL = "http://exam.ioe.edu.np"
DATE_FORMAT = "%A, %B %d, %Y"
TIMEZONE = ZoneInfo("Asia/Kathmandu")

def parse_date(date):
    return datetime.strptime(date, DATE_FORMAT).astimezone(TIMEZONE)


res = requests.get(URL)
if res.ok:
    soup = BeautifulSoup(res.text, "html.parser")
    table = soup.find(id = "datatable")
    rows = table.find_all("tr")

    fg = FeedGenerator()
    fg.id(URL)
    fg.title('IOE Exam Website RSS Feed')
    fg.link( href=URL )
    fg.logo(URL+"/favicon.ico")
    fg.description("Scrapes exam.ioe.edu.np and generates RSS feed of notices")

    for row in map(lambda r: r.find_all("td"), rows[1:]):
        item = fg.add_entry(order="append")

        item.title(row[1].get_text().strip())

        id = row[3].find("a").get("href").split("/")[-1]
        item.id(id)

        date = parse_date(row[2].get_text().strip())
        item.published(date)

        link = URL + row[1].find("a").get("href")
        item.link(href=link)

    fg.rss_file('rss.xml', pretty=True)
    fg.atom_file('atom.xml', pretty=True)
