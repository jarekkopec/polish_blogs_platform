import datetime
from pathlib import Path
import csv
import shutil
import html

import pandas as pd
import yaml
import feedparser
from yattag import Doc
import pytz



local_html = Path(__file__).resolve().parent.parent / "frontend" / "index.html"
served_html = Path("/var/www/html/index.html")

def clean_string(string):
    fixed = html.unescape(string)
    return(fixed)

def read_sites():
    sites_path = Path(__file__).resolve().parent / "sites.yml"
    with open(sites_path, "r", encoding="utf-8") as file:
        sites = yaml.safe_load(file)
    return sites

def parse_site(url):
    posts = []
    feed = feedparser.parse(url)

    site_title = clean_string(feed.feed.title)
    site_link = feed.feed.link
    
    entries = feed["entries"]
    
    for el in entries[:10]:
        date_object = datetime.datetime(*el.published_parsed[0:6])
        date_string = date_object.strftime("%d-%m-%Y %H:%M:%S")
        
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
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y %H:%M:%S")
    df = df.sort_values(by="date", ascending=False)
    
    grouped = df.groupby('site_title')
    result = []
    for site_title, group in grouped:
        result.append({
            'site_title': site_title,
            'site_link': group.iloc[0]['site_link'],
            'posts': group[['post_link', 'title', 'date', 'summary']].to_dict(orient='records')
        })
    return result

def render(content):
    doc, tag, text = Doc().tagtext()

    doc.asis("<!DOCTYPE html>")
    with tag("html"):
        with tag("head"):
            doc.stag("meta", charset = "utf-8")
            doc.stag("meta",
                     name="viewport",
                     content="width=device-width, initial-scale=1.0")
            doc.stag("link", rel="stylesheet", href="assets/style.css")
            with tag("script",
                     src="https://cdn.jsdelivr.net/npm/sortablejs@1.15.0/Sortable.min.js"):
                text("")
            with tag("script", src="assets/scripts.js"):
                text("")
        with tag("body"):
            with tag("header"):
                with tag("h1", id = "site_name"):
                    text("Polskie blogi")
            with tag("content"):
                for i, blog in enumerate(content):
                    with tag("div", id="blog-" + str(i+1)):
                        with tag("h2"):
                            text(blog["site_title"])
                        with tag("ul"):
                            for post in blog["posts"]:
                                with tag("li"):
                                    with tag("a", href=post["post_link"]):
                                        text(post["title"])
            with tag("footer"):
                utc_now = datetime.datetime.now(pytz.utc)
                warsaw_tz = pytz.timezone("Europe/Warsaw")
                warsaw_time = utc_now.astimezone(warsaw_tz)
                warsaw_time_string = warsaw_time.strftime('%Y-%m-%d %H:%M:%S')
                text(f"Ostatnia aktualizacja: {warsaw_time_string}")


    with open(local_html, "w") as file:
        content = doc.getvalue()
        file.write(content)

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



if __name__ == "__main__":
    main()
