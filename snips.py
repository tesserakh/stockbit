#!/usr/bin/env python3
""" Daily Snips Stockbit News Scraper
Get recent newsletter from the largest stock investment platform
in Indonesia, Stockbit.
"""
from bs4 import BeautifulSoup
from datetime import datetime
import unicodedata
import argparse
import requests
import csv, os

def scrape(session, tag=None, category='recent', save=False):
    # handle query
    baseurl = 'https://snips.stockbit.com'
    slug_category = '/snips-terbaru' if category == 'recent' else f'/{category}'
    if tag is not None:
        if len(tag) == 4 and tag == tag.upper():
            slug_tag = tag
        else:
            slug_tag = tag.title().replace(' ','+')
        endpoint = f"/tag/{slug_tag}#show-archive"
    else:
        endpoint = ''
    try:
        # interact with the web
        response = session.get(baseurl + slug_category + endpoint)
        print(f'({response.status_code}) {response.url}')
        if response.status_code != 200:
            print("""
        No article found.
        
        You can use a ticker or a keyword for tag and keep category as default (recent news).
        Tag examples: ANTM, TLKM, UNVR (in uppercase)
                      inflasi, konstruksi (single word)
                      'batu bara', 'mobil listrik' (multiple word)
        """)
        # parse html
        soup = BeautifulSoup(response.text, 'html.parser')
        newsletter = parse(soup)
        # define data structure
        header_fields = ['published', 'headline', 'description', 'tags', 'url', 'timestamp']
        timestamp = datetime.utcnow().isoformat()[:-7].replace('T',' ')
        data = [header_fields]
        for article in newsletter:
            row = article + [timestamp]
            data.append(row)
        # save result as a csv file
        if save and len(data) > 1:
            save_dir = 'recent'
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            filename = f"stockbit_snips_{timestamp.replace(':','-').replace(' ', '_')}.csv"
            save_path = os.path.join(save_dir, filename)
            with open(save_path, 'w') as fout:
                csv_writer = csv.writer(fout)
                csv_writer.writerows(data)
            print(f"Data saved to {save_path}")
        return
    except Exception as e:
        print(f'ERROR: {e}')
        return

def parse(soup):
    baseurl = 'https://snips.stockbit.com'
    articles = soup.find_all('article')
    if articles == None:
        newsletter = None
    else:
        newsletter = []
        for item in articles:
            # parse items
            h1 = item.find('h1').find('a', href=True)
            headline = unicodedata.normalize('NFKD', h1.get_text())
            url = baseurl + h1['href']
            published = item.find('time', {'class':'published'})['datetime']
            published_dt = datetime.strptime(published, '%Y-%m-%d')
            description = item.find('p').get_text()
            tags = ', '.join([i.get_text() for i in item.find_all('a', {'rel':'tag'})])
            # expose newsletter
            print('[{}] {} <{}>'.format(published, headline, url))
            # save newsletter list
            newsletter.append([published, headline, description, tags, url])
    return newsletter

if __name__ == '__main__':
    used_arguments = argparse.ArgumentParser()
    used_arguments.add_argument('-t', '--tag', required=False, default=None, help="tag or keyword of the feeds")
    used_arguments.add_argument('-c', '--cat', required=False, default='recent', help="feed's category")
    used_arguments.add_argument('-s', '--save', action='store_true', help="save result to a csv file")
    args = vars(used_arguments.parse_args())
    session = requests.Session()
    scrape(session, tag=args['tag'], category=args['cat'], save=args['save'])

