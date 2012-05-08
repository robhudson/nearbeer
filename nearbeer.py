import json
import os

from flask import Flask, make_response, render_template
import slumber


UNTAPPD_URL = 'http://api.untappd.com/v3'
UNTAPPD_KEY = os.environ.get('UNTAPPD_API_KEY')
API = slumber.API(UNTAPPD_URL)
MAX_BREWERIES = 5

from geo import venues_near

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/beers/<ll>')
def beers(ll):
    vens = venues_near(ll)
    breweries = get_breweries(vens[:MAX_BREWERIES])
    return render_template('beer.html', breweries=breweries)


@app.route('/manifest.webapp')
def manifest():
    data = {
        'name': 'Near Beer',
        'description': 'Find good beer near you.',
        'developer': {
            'name': '',
            'url': '',
        },
        'icons': {
        },
        'locales': {},
        'default_locale': 'en-US'
    }
    resp = make_response(json.dumps(data))
    resp.headers['mimetype'] = 'application/x-web-app-manifest+json'
    return resp


def get_breweries(venues):
    """
    Given a list of brewery names, query each.

    Brewery names are assumed to be in order from closest to farthest.
    """
    breweries = []
    for q in venues:
        res = API.brewery_search.get(key=UNTAPPD_KEY, q=q['name'])
        for brewery in res['results']:
            breweries.append(brewery)
    return breweries

def _get_top(brewery_ids, exclude=None):
    """
    Given a list of brewery IDs, find the top overall beer.

    If exclude (a list) is provided, ignore these brewery IDs from the results.
    """
    # Get top beers from each brewery.
    beers = {}
    bids = [bid for bid in brewery_ids if bid not in exclude]
    for bid in brewery_ids:
        res = API.brewery_info.get(key=UNTAPPD_KEY, brewery_id=bid)
        for beer in res['results']['top_beers']:
            beers[beer['beer_id']] = {}

    # Find the top beer by weekly_count.
    cnt = 0
    top_beer = None
    for bid in beers:
        res = API.beer_info.get(key=UNTAPPD_KEY, bid=bid)
        weekly_count = int(res['results']['weekly_count'])
        beers[bid]['weekly_count'] = weekly_count
        if weekly_count > cnt:
            cnt = weekly_count
            top_beer = res

    return top_beer


if __name__ == '__main__':
    app.run(debug=True)
