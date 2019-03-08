#!/usr/bin/env python3
import os.path
import sys
import feedparser
import diaspy  # git clone https://github.com/marekjm/diaspy.git ; cd diaspy; sudo python3 setup.py install
import json
import requests
import re
import sqlite3
from datetime import datetime, date, time, timedelta
import urllib.request

if len(sys.argv) < 4:
    print("Usage: python3 twitter2diaspora.py twitter_account diaspora_login diaspora_passwd diaspora_instance")
    sys.exit(1)

# sqlite db to store processed tweets (and corresponding toots ids)
sql = sqlite3.connect('twitter2diaspora.db')
db = sql.cursor()
db.execute('''CREATE TABLE IF NOT EXISTS tweets (tweet text, twitter text, mastodon text, instance text)''')

if len(sys.argv)>5:
    days = int(sys.argv[5])
else:
    days = 1

twitter = sys.argv[1]
poduser = sys.argv[2]
poduserpwd = sys.argv[3]
instance = sys.argv[4]
aspect_to_post = "public"
mastodon_api = None

d = feedparser.parse('http://twitrss.me/twitter_user_to_rss/?user='+twitter)

for t in reversed(d.entries):
    # check if this tweet has been processed
    db.execute('SELECT * FROM tweets WHERE tweet = ? AND twitter = ?  and mastodon = ? and instance = ?',(t.id, twitter, poduser, instance))
    last = db.fetchone()

    # process only unprocessed tweets less than 1 day old
    if last is None and (datetime.now()-datetime(t.published_parsed.tm_year, t.published_parsed.tm_mon, t.published_parsed.tm_mday, t.published_parsed.tm_hour, t.published_parsed.tm_min, t.published_parsed.tm_sec) < timedelta(days=days)):
        
        #h = BeautifulSoup(t.summary_detail.value, "html.parser")
        c = t.title
        if t.author != '(%s)' % twitter:
            c = ("RT %s\n" % t.author[1:-1]) + c

        # replace t.co link by original URL
        m = re.search(r"http[^ \xa0]*", c)
        if m != None:
            l = m.group(0)
            r = requests.get(l, allow_redirects=False)
            if r.status_code in {301,302}:
                c = c.replace(l,r.headers.get('Location'))

        # remove pic.twitter.com links
        m = re.search(r"pic.twitter.com[^ \xa0]*", c)
        if m != None:
            l = m.group(0)
            c = c.replace(l,' ')

        # remove ellipsis
        textmessage = c.replace('\xa0…',' ')

        connection = diaspy.connection.Connection(pod=instance, username=poduser, password=poduserpwd)
        connection.login()
        token = repr(connection)
        stream = diaspy.streams.Stream(connection)

        # get the pictures...
        toot_media = []
        for p in re.finditer(r"https://pbs.twimg.com/[^ \xa0\"]*", t.summary):
            urllib.request.urlretrieve(p.group(0), "twitterbot-tmp.jpg")
            photoid = stream._photoupload(filename="twitterbot-tmp.jpg")
            toot_media.append(photoid)
            
        if toot_media is not None:
            stream.post(photos=toot_media, text=textmessage, aspect_ids=aspect_to_post)           
            toot="id"
            if "id" in toot:
                db.execute("INSERT INTO tweets VALUES ( ? , ? , ? , ? )",
                (t.id, twitter, poduser, instance))
                sql.commit()
