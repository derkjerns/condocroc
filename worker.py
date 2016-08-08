"""
Demonstrates how to use the background scheduler to schedule a job that executes on 3 second
intervals.
"""
import os
import time
import feedparser
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from models import *

def fetch_new_cg_listings():
    cgfeed = feedparser.parse('https://toronto.craigslist.ca/search/tor/apa?bedrooms=2&format=rss&max_price=2600')
    notify = False
    for entry in cgfeed.entries:
        existing = Listing.query.filter_by(url=entry.link).first()
        if existing is None:
            notify = True
            date = datetime.strptime(entry.published[:-6], "%Y-%m-%dT%H:%M:%S").strftime("%B %d, %Y")
            listing = Listing(entry.title, entry.link, entry.summary, date)
            db.session.add(listing)
    db.session.commit()
    if notify:
        notify_me()

def notify_me():
    print ("text 416 571 0806")


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_new_cg_listings, 'interval', minutes=30)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
    fetch_new_cg_listings()

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()