import datetime
from pathlib import Path
import csv
import shutil
import html

import pandas as pd
import yaml
import feedparser
from yattag import Doc



local_html = Path(__file__).resolve().parent / 'index.html'
served_html = Path('/var/www/html/index.html')

def clean_string(string):
    fixed = html.unescape(string)
    return(fixed)

def read_sites():
    sites_path = Path(__file__).resolve().parent / 'sites.yml'
    with open(sites_path, 'r', encoding='utf-8') as file:
        sites = yaml.safe_load(file)
    return sites

def parse_site(url):
    posts = []
    feed = feedparser.parse(url)

    site_title = clean_string(feed.feed.title)
    site_link = feed.feed.link
    
    entries = feed["entries"]
    
    for el in entries:
        date_object = datetime.datetime(*el.published_parsed[0:6])
        date_string = date_object.strftime('%d-%m-%Y %H:%M:%S')
        
        post_date = date_string
        post_title = clean_string(el.title)
        post_summary = clean_string(el.summary)
        post_link = el.link

        posts.append({
            "site_title": site_title,
            "site_link": site_link,
            "post_link": post_link,
            "title": post_title,
            "date": post_date,
            "summary": post_summary
        })
    
    return posts

def compose(sites_content):
    
    df = pd.DataFrame(sites_content)
    df["date"] = pd.to_datetime(df["date"], format='%d-%m-%Y %H:%M:%S')
    df = df.sort_values(by="date", ascending=False)
    
    return df.to_dict(orient="records")

def render(content):
    doc, tag, text = Doc().tagtext()
    with tag('html'):
        with tag('body'):
            with tag('table'):
                for el in content:
                    with tag("tr"):
                        with tag("td"):
                            with tag("a", href = el["site_link"]):
                                text(el["site_title"])
                        with tag("td"):
                            with tag("a", href = el["post_link"]):
                                text(el["title"])
                        with tag("td"):
                            text(el["summary"][:100] + "...")


    with open(local_html, "w") as file:
        file.write(doc.getvalue())

def push():
    src = local_html
    dst = served_html
    shutil.copy(src, dst)


def main():
    sites = read_sites()["sites"]
    sites_content = []
    for s in sites:
        try:
            site_content = parse_site(s.get("url"))
            sites_content += site_content
        except:
            continue
    c = compose(sites_content)
    render(c)
    push()



if __name__ == '__main__':
    main()