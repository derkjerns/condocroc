import os
from flask import Flask, render_template, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
import datetime as datetime
from lxml import html
import requests

# initialization
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.context_processor
def inject_current_year():
    year = datetime.datetime.now().year
    return dict(year=year)


from models import *


# controllers
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'ico/favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(405)
@app.errorhandler(401)
@app.errorhandler(500)
def http_error_handler(e):
    return render_template('error.html', error=e), e.code


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/listings")
def listings():
    listings = Listing.query.order_by(Listing.id.desc()).all()
    return render_template('listings.html', listings=listings)

@app.route("/parsecg")
def parsecg():
    url = request.args.get('url')
    page = requests.get(url)
    tree = html.fromstring(page.content)
    title = tree.xpath('//span[@id="titletextonly"]/text()')[0]
    price = tree.xpath('//span[@class="price"]/text()')[0]
    description = tree.xpath('//section[@id="postingbody"]/text()')[0]
    mains = tree.xpath('//a[@class="thumb"]/@href')
    thumbs = tree.xpath('//a[@class="thumb"]/img/@src')
    images = []
    for a,b in zip(mains, thumbs):
        images.append([a,b])
    return render_template('cgpage.html', title=title, price=price, description=description, images=images)

# launch
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
