import os
import re
from flask import Flask
from flask import render_template, request, jsonify, send_from_directory
from os import listdir
from os.path import isfile, join
app = Flask(__name__)


@app.route('/')
def init():
	return render_template('drag.html', cards=get_all_cards())

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/_get_filtered_cards')
def get_filtered_cards():
	search_string = request.args.get('search_string')
	prefixed_cards = [filename for filename in listdir('static/images/library/') if (not (filename.startswith('.')) and (re.search(search_string, filename, re.IGNORECASE) ))]
	prefixed_cards.sort()
	return render_template('card-list.html', cards=prefixed_cards)

@app.route('/_get_all_cards')
def get_all_cards():
	return render_template('card-list.html', cards=get_all_cards())

def get_all_cards():
	cards = [filename for filename in listdir('static/images/library/') if (isfile(join('static/images/library/', filename)) and not (filename.startswith('.')))]
	cards.sort()
	return cards

@app.route('/_get_dropped_card_template')
def get_dropped_card():
	img_src = request.args.get('img_src', '')
	return render_template('dropped-card.html', img_src=img_src)
