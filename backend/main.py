import datetime
from pathlib import Path
import csv

import yaml
import feedparser
# import sqlite3



def read_sites():
    sites_path = Path(__file__).resolve().parent / 'sites.yml'
    with open(sites_path, 'r', encoding='utf-8') as file:
        sites = yaml.safe_load(file)
    return sites

def parse_site(url):
    posts = []
    feed = feedparser.parse(url)

    site_title = feed.feed.title
    site_link = feed.feed.link
    
    entries = feed["entries"]
    
    for el in entries:
        date_object = datetime.datetime(*el.published_parsed[0:6])
        date_string = date_object.strftime('%d-%m-%Y %H:%M:%S')
        
        post_date = date_string
        post_title = el.title
        post_summary = el.summary

        posts.append({
            "site_title": site_title,
            "site_link": site_link,
            "title": post_title,
            "date": post_date,
            "summary": post_summary
        })
    
    return posts


def write_db(content):
    db_path = Path(__file__).resolve().parent / 'blogs.csv'
    with open(db_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "site_title", "site_link", "title", "date", "summary"])
        writer.writerows(content)

    # db_path = Path(__file__).resolve().parent / 'blogs.db'
    # conn = sqlite3.connect(db_path)
    # for c in content:
    #     cursor = conn.cursor()
    #     cursor.execute('''
    #         CREATE TABLE IF NOT EXISTS posts (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             title TEXT,
    #             date TEXT,
    #             summary TEXT
    #         )
    #     ''')
    #     cursor.execute(
    #         'INSERT INTO posts (title, date, summary) VALUES (?, ?, ?)',
    #         (c.get('title'), c.get('date'), c.get('summary'))
    #     )
    #     conn.commit()
    # conn.close()


def main():
    sites = read_sites()["sites"]
    for s in sites:
        write_db(parse_site(s.get('url')))



if __name__ == '__main__':
    main()