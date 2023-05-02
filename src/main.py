"""Start file for my flask app"""
from flask import Flask, render_template
from classes import Aftonbladet, Gp, Klart, Yr


app = Flask(__name__, template_folder='templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/klart')
def klart():
    return render_template('klart.html', klart_weather=Klart.get_klart_weather(self=Klart()))


@app.route('/yr')
def yr():
    return render_template('yr.html', yr_weather=Yr.get_yr_weather(self=Yr()))


@app.route('/gp')
def gp():
    return render_template('gp.html', gp_articles=Gp.get_gp_articles(self=Gp()))


@app.route('/aftonbladet')
def aftonbladet():
    return render_template('aftonbladet.html',
                           aftonbladet_articles=Aftonbladet.get_aftonbladet_articles(self=Aftonbladet()))


app.run(debug=True)
