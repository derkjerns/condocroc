"""
Demonstrates how to use the background scheduler to schedule a job that executes on 3 second
intervals.
"""
import os
import time
import feedparser
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from twilio.rest import TwilioRestClient
from models import *

account_sid = "ACf35e649699bce65387ceadef2a328ebd"
auth_token = "14b49654235ea385f9453cf6a1a7206c"
client = TwilioRestClient(account_sid, auth_token)

neg_word_list = ['3bd', '3 bd', '3bed', '3 bed', '3br', '3 br',
                 'harbord', 'bloor', 'dupont', 'davenport', 'st. clair',
                 'avenue', 'church', 'jarvis', 'sherbourne', 'broadview',
                 'parliament', 'yonge', 'eglinton', 'roncesvalles',
                 'lawrence', 'rosedale', 'sheppard']

def fetch_new_cg_listings():
    cgfeed = feedparser.parse('https://toronto.craigslist.ca/search/tor/apa?bedrooms=1&format=rss&hasPic=1&max_price=2600&minSqft=900&min_price=2000')
    notify = False
    for entry in cgfeed.entries:
        if not any(word in entry.title.lower() for word in neg_word_list):
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
    client.messages.create(to="+14165710806", from_="+16475034607",
                           body="New listings! https://condocroc.herokuapp.com")


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_new_cg_listings, 'interval', minutes=60)
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
