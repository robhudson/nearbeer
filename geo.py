import os

import foursquare


FSQ_CLIENT_ID = os.environ.get('FSQ_CLIENT_ID')
FSQ_CLIENT_SECRET = os.environ.get('FSQ_CLIENT_SECRET')
FSQ_CATEGORIES = [
    '4d4b7105d754a06374d81259', # Food
    '4d4b7105d754a06376d81259', # Nightlife Spot
    '4d4b7104d754a06370d81259', # Arts & Entertainment
]

client = foursquare.Foursquare(client_id=FSQ_CLIENT_ID,
                               client_secret=FSQ_CLIENT_SECRET)


def venues_near(ll):
    """
    ll = comma separated lat,long. e.g. '36.962452,-122.02446'
    """
    return client.venues.search(params={
        'll': ll,
        'categoryId': ','.join(FSQ_CATEGORIES),
    })
