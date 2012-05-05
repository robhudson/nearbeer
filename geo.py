import os

import foursquare


FSQ_CLIENT_ID = os.environ.get('FSQ_CLIENT_ID')
FSQ_CLIENT_SECRET = os.environ.get('FSQ_CLIENT_SECRET')
FSQ_CATEGORIES = [
    '4bf58dd8d48988d1d7941735', # Breweries
]


def brewery_names_near(ll):
    """ Return a list of  """
    venues = venues_near(ll)
    return [b['name'] for b in venues]


def venues_near(ll):
    """
    ll = comma separated lat,long. e.g. '36.962452,-122.02446'
    """
    client = foursquare.Foursquare(client_id=FSQ_CLIENT_ID,
                                   client_secret=FSQ_CLIENT_SECRET)

    return client.venues.search(params={
        'll': ll,
        'categoryId': ','.join(FSQ_CATEGORIES),
        'radius': 8000,
    })['venues']
