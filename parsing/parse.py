from requests import get
from bs4 import BeautifulSoup
import json
from urllib.parse import urlparse
import cfscrape
from analyze import get_orgs_from_text, classify
import dateparser
import re
import datetime




def get_site_info(url):
    name = urlparse(url).hostname
    for s in sites['sites']:
        if urlparse(s['URL']).hostname == name:
            return s
    return {"URL": None}

def str_to_date(text):
    for i in range(len(text)):
        if text[i].isdigit():
            break
    d = dateparser.parse(text[i:])
    return d.strftime("%d.%m.%Y")

def parse(url, keywords=None):
    if not keywords:
        keywords = ["технологии", "импортозамещение", "инновации",
                    "научные разработки", "патенты",
                    "гранты", "исследования"]
    try:
        scraper = cfscrape.create_scraper(delay=5)
        response = scraper.get(url) #,  headers={"useragent": f"{ua.random}"})

        if response:
            soup = BeautifulSoup(response.text, "lxml")
            site_info = get_site_info(url)
            if site_info["URL"]:
                #title = soup.find(class_=site_info["title"]).text
                title = soup.select_one(site_info["title"]).text
                title = title.replace('\n', " ").replace('\t', " ").strip()
                date = soup.select_one(site_info["date"]).text
                date = date.replace('\n', " ").replace('\t', " ").strip()
                date = str_to_date(date)
                text = soup.select_one(site_info["text"]).get_text()
                text = text.replace('\n', " ").replace('\t', " ").strip()
                classes = classify(text, keywords)
                orgs = get_orgs_from_text(text)
                return 1, \
                       {"org": orgs,
                        "name": urlparse(url).hostname,
                        "title": title,
                        "date": date,
                        "URL": url,
                        "text": text,
                        "keywords": classes
                }
            else:
                title = soup.find("h1")
                if not title:
                    title = soup.find(class_=re.compile("title"))
                if not title:
                    title = soup.find(class_=re.compile("header"))
                if not title:
                    title = soup.find(class_=re.compile("intro"))
                if not title:
                    title = ""
                else:
                    title = title.text.replace('\n', " ").replace('\t', " ").strip()
                date = soup.find(class_=re.compile("date"))
                if date:
                    date = date.text.replace('\n', " ").replace('\t', " ").strip()
                else:
                    date = "today"
                date = str_to_date(date)
                text = soup.find(class_=re.compile("detail"))
                if not text:
                    text = soup.find(class_=re.compile("content"))
                if not text:
                    text = soup.find(class_=re.compile("text"))
                if not text:
                    text = soup
                text = text.get_text()
                text = text.replace('\n', " ").replace('\t', " ").strip()
                classes = classify(text, keywords)
                orgs = get_orgs_from_text(text)
                return 1, \
                       {"org": orgs,
                        "name": urlparse(url).hostname,
                        "title": title,
                        "date": date,
                        "URL": url,
                        "text": text,
                        "keywords": classes
                }
        else:
            return 0, {"Error_code": response.status_code}
    except Exception as err:
        return 0, {"Error": str(err)}


try:
    sites = json.load(open('../static/sites.json', encoding='utf-8'))
except:
    sites = {
        "sites": [
                    ]
    }
