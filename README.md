# twitter2diaspora*

A small python 3.x script to replicate tweets on a Diaspora pod. 
It is based on https://github.com/cquest/tootbot by Christian Quest

The script only need Diaspora login/pass to post toots.

It gets the tweets from RSS available at http://twitrss.me, then does some cleanup on the content:
- twitter tracking links (t.co) are dereferenced
- twitter hosted pictures are retrieved and uploaded to Diaspora

A sqlite database is used to keep track of tweets than have been posted.


The script is simply called by a cron job and can run on any server.

## Setup

```
# install diaspy
git clone https://github.com/marekjm/diaspy.git
cd diaspy
sudo python3 setup.py install
cd ..

# clone this repo
git clone https://github.com/produnis/twitter2diaspora.git
cd twitter2diaspora

# install other required python modules
sudo pip3 install -r requirements.txt
```

## Useage

`python3 twitter2diaspora.py <twitter_pseudo> <diaspora_username> <diaspora_password> <diaspora_domain>`

Example:

`python3 twitter2diaspora.py s04 s04bot **password** https://diasp.eu`

It's up to you to add this in your crontab :)
