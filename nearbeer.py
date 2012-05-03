import os

from flask import Flask, render_template
import slumber


UNTAPPD_URL = 'http://api.untappd.com/v3'
UNTAPPD_KEY = os.environ.get('UNTAPPD_API_KEY')
API = slumber.API(UNTAPPD_URL)

top_1 = {u'brewery_id': u'1126', u'beer_creator': u'Untappd Team', u'name': u'Blur IPA', u'img': u'https://untappd.s3.amazonaws.com/site/assets/images/temp/badge-beer-default.png', u'total_count': u'29', u'avg_rating': 2, u'weekly_count': u'3', u'unique_count': u'25', u'beer_creator_id': u'13097', u'beer_created': u'Sat, 21 Aug 2010 07:26:35 +0000', u'beer_id': u'270', u'monthly_count': u'5', u'type': u'American IPA', u'brewery': u'Seabright Brewery', u'beer_abv': u'0'}
top_2 = {u'brewery_id': u'3731', u'beer_creator': u'josh h.', u'name': u'India Pale Ale', u'img': u'https://untappd.s3.amazonaws.com/site/assets/images/temp/badge-beer-default.png', u'total_count': u'81', u'avg_rating': 3, u'weekly_count': u'4', u'unique_count': u'69', u'beer_creator_id': u'7372', u'beer_created': u'Tue, 21 Dec 2010 13:28:02 +0000', u'beer_id': u'15944', u'monthly_count': u'13', u'type': u'Imperial / Double IPA', u'brewery': u'Santa Cruz Mountain Brewing', u'beer_abv': u'7.5'}
top_3 = {u'brewery_id': u'9955', u'beer_creator': u'Richard J.', u'name': u'Dark Night Oatmeal Stout', u'img': u'https://untappd.s3.amazonaws.com/site/assets/images/temp/badge-beer-default.png', u'total_count': u'83', u'avg_rating': 3, u'weekly_count': u'2', u'unique_count': u'76', u'beer_creator_id': u'8482', u'beer_created': u'Sun, 26 Dec 2010 06:34:05 +0000', u'beer_id': u'17584', u'monthly_count': u'20', u'type': u'Oatmeal Stout', u'brewery': u'Santa Cruz Ale Works', u'beer_abv': u'0'}


app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('home.html', **{
        'tops': [top_1, top_2, top_3],
    })


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
