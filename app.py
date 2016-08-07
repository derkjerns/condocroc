import os
from flask import Flask, render_template, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import abort

# initialization
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

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
    listings = Listing.query.all()
    return render_template('index.html', listings=listings)


@app.route("/cg", methods=['POST'])
def addCraigslistListing():
    if request.method == 'POST':
        try:
            json = request.get_json()
            listing = Listing(json['title'],json['url'],json['description'],json['date'])
            db.session.add(listing)
            db.session.commit()
        except Exception, e:
            abort(500)
    return render_template('success.html')


# launch
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
