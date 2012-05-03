from flask import Flask, render_template

from geo import venues_near

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/beers/<ll>')
def beers(ll):
    vens = venues_near(ll)
    return render_template('beer.html')


if __name__ == '__main__':
    app.run()
