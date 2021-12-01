import sys
import os, os.path

from flask import Flask, render_template, redirect, url_for, request, flash

from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import whoosh
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import *
from whoosh.qparser import QueryParser
from whoosh.qparser import MultifieldParser
from whoosh import qparser
from whoosh import fields, index, qparser


import pandas as pd
from whoosh.fields import Schema, TEXT
from whoosh import index
import sys
import csv
import math

csv.field_size_limit(sys.maxsize)




app = Flask(__name__)

app.config['SECRET_KEY'] = 'NOJERRYSALLOWEDbcSHBXUXs2123'

bootstrap =Bootstrap(app)

@app.route('/', methods=['GET', 'POST']) #main index page 
def index():

	return render_template('welcome_page.html')



@app.route('/next/<qp>/<pp>' , methods=["GET", "POST"])
def next(qp,pp):
	global mysearch
	data = request.form 	#pass the variables of the search to next , get page and increment it

	keywordquery = qp
	int(pp)

	page = int(pp)

	
	artist_id, artist, album, album_release, track, artist_image, album_art, preview_link, link_tosong, lyrics, related_artists, artist_genres, date_released, page,  Results = mysearch.index_search(keywordquery,page+1)
	
	pag = math.ceil(Results/10) # passing the number of results so that the #number of pages shows 

	if page == pag: #
		page -=1	# SO IT DOESNT PASS THE TOTAL NUMBER OF PAGES
		return render_template('results.html', query=keywordquery, len = len(artist), pag = pag , page = page, artist_id = artist_id, artist= artist, album =album, album_release =album_release, artist_image= artist_image, album_art = album_art, 
		 preview_link = preview_link, link_tosong =link_tosong, lyrics =lyrics, related_artists = related_artists, artist_genres =artist_genres,date_released =date_released)

	else:
		return render_template('results.html', query=keywordquery, len = len(artist), pag = pag , page = page, artist_id = artist_id, artist= artist, album =album, album_release =album_release, artist_image= artist_image, album_art = album_art, 
		 preview_link = preview_link, link_tosong =link_tosong, lyrics =lyrics, related_artists = related_artists, artist_genres =artist_genres,date_released =date_released)



@app.route('/previous/<q>/<p>' , methods=["GET", "POST"])
def previous(q,p):
	global mysearch
	data = request.form

	
	keywordquery = q
	int(p)

	page = int(p)


	if page <=1:
		page==2
		
		artist_id, artist, album, album_release,track, artist_image, album_art, preview_link, link_tosong, lyrics, related_artists, artist_genres, date_released, page,  Results = mysearch.index_search(keywordquery,page)
		
		pag = math.ceil(Results/10)

		return render_template('results.html', query=keywordquery, len = len(artist), pag = pag , page = page, artist_id = artist_id, artist= artist, album =album, album_release =album_release, artist_image= artist_image, album_art = album_art, 
		 preview_link = preview_link, link_tosong =link_tosong, lyrics =lyrics, related_artists = related_artists, artist_genres =artist_genres,date_released =date_released)

	else:
		print(page)
		artist_id, artist, album, album_release, artist_image, album_art, preview_link, link_tosong, lyrics, related_artists, artist_genres, date_released, page,  Results = mysearch.index_search(keywordquery,page-1)

		pag = math.ceil(Results/10)

		return render_template('results.html', query=keywordquery, len = len(artist), pag = pag , page = page, artist_id = artist_id, artist= artist, album =album, album_release =album_release, artist_image= artist_image, album_art = album_art, 
		 preview_link = preview_link, link_tosong =link_tosong, lyrics =lyrics, related_artists = related_artists, artist_genres =artist_genres,date_released =date_released)

	


@app.route('/results/', methods=['GET', 'POST'])
def results():
	global mysearch
	page = 1
	if request.method == 'POST':
		data = request.form

	else:
		data = request.args

	keywordquery = data.get('searchterm')
	

	artist_id, artist, album, album_release,track, artist_image, album_art, preview_link, link_tosong, lyrics, related_artists, artist_genres, date_released, page,  Results = mysearch.index_search(keywordquery,page)
	
	pag = math.ceil(Results/10)

	if Results == 0:
		flash("Not in the search, try again")
		return render_template('welcome_page.html')
	else:
		return render_template('results.html', query=keywordquery, len = len(artist), pag = pag , page = page, artist_id = artist_id, artist= artist, album =album, album_release =album_release, track = track, artist_image= artist_image, album_art = album_art, 
		 preview_link = preview_link, link_tosong =link_tosong, lyrics =lyrics, related_artists = related_artists, artist_genres =artist_genres,date_released =date_released)


@app.route('/priceFilter/<q3>/<p3>', methods=['GET', 'POST'])
def priceFilter(q3,p3):
	global mysearch

	page = int(p3)
	keywordquery = q3 #sends the query and page to the price_search function where it sorts the pricing of that query

	item, description, picture, productType, brand, size, price, url, onsale, discount, page, Results = mysearch.price_search(keywordquery,page)
	
	pag = math.ceil(Results/10)

	return render_template('results.html', query=keywordquery, len = len(artist), pag = pag , page = page, item =item, description= description, picture =picture, productType = productType, brand = brand, size = size, price =price, url =url, onsale = onsale, discount =discount)


#approutes=============================================================================
	



# import data into pandas df and create index schema

class wooshSearch(object):

	def __init__(self):
		super(wooshSearch,self).__init__()


	def index(self):
		
		with open(r"finalwlyricsexample.csv",encoding="utf8") as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			df = pd.DataFrame([csv_reader], index=None) 
			df.head() 
		schema = Schema(artist_id=TEXT(stored=True), artist=TEXT(stored=True), album=TEXT(stored = True),album_release=TEXT(stored = True),track =TEXT(stored = True),artist_image=TEXT(stored = True),album_art=TEXT(stored = True),preview_link=TEXT(sortable=True),link_tosong=TEXT(stored = True),lyrics=TEXT(stored = True),related_artists=TEXT(stored = True),artist_genres=TEXT(stored = True),date_released=TEXT(stored = True))
		
		ix = create_in('exampleIndex', schema)
		
		# Imports stories from pandas df
		
		
		for i in range(len(list(df))):		#go the length of the index

			for val in list(df[i]):

				writer = ix.writer() 		#add documents

				writer.add_document(artist_id=(val[0]),	#val[] are the positions in the index piping it to the schema
						   artist =(val[1]),
						   album =(val[2]),
						   album_release =(val[3]),
						   track=(val[4]),
						   artist_image =(val[5]),
						   album_art =(val[6]),
						   preview_link =(val[7]),
						   link_tosong =(val[8]),
						   lyrics =(val[9]),
						   related_artists = (val[10]),
						   artist_genres = (val[11]),
						   date_released = (val[12]))

				writer.commit()
				self.ix = ix

				print ("writing doc",i)

										#commit the document
   
	# creates index searcher

	def index_search(self,queryEntered,page):

		artist_id = list()
		artist = list()
		album= list()
		album_release= list()
		track = list()
		artist_image= list()
		album_art= list()
		preview_link= list()
		link_tosong= list()
		lyrics= list()
		related_artists= list()
		artist_genres= list()
		date_released= list()






		ix = open_dir('exampleIndex')
		schema = ix.schema
		# Create query parser that looks through designated fields in index
		og = qparser.OrGroup.factory(0.9)
		mp = qparser.MultifieldParser(['artist_id', 'artist','album','album_release','track','artist_image','album_art','preview_link','link_tosong','lyrics','related_artists','artist_genres','date_released'], schema =self.ix.schema, group = og)


		q = mp.parse(queryEntered)
		#threshold = int(input("How many results would you like?:"))
		# Actual searcher, prints top 10 hits
		with ix.searcher() as s:
			results = s.search_page(q, page)	#user threshold
			print("Search Results: ")
			try:
				for i in results:
					#print("\n RESULT #:",i+1 )			#prints resuts 
					#print(results[i])
					#print("\n")

					artist_id.append(i['artist_id'])
					artist.append(i['artist'])
					album.append(i['album'])
					album_release.append(i['album_release'])
					track.append(i['track'])
					artist_image.append(i['artist_image'])
					album_art.append(i['album_art'])
					preview_link.append(i['preview_link'])
					link_tosong.append(i['link_tosong'])
					lyrics.append(i['lyrics'])
					related_artists.append(i['related_artists'])
					artist_genres.append(i['artist_genres'])
					date_released.append(i['date_released'])

			except IndexError:							#if it doesnt find x number of results it catches the error 
				pass									#program goes into the infinite while loop for another query
		return  artist_id, artist, album, album_release,track, artist_image, album_art, preview_link, link_tosong, lyrics, related_artists, artist_genres, date_released , page, len(results)


	def price_search(self,queryEntered,page):

		item = list()
		description = list()
		picture= list()
		productType= list()
		brand= list()
		size= list()
		price= list()
		url= list()
		onsale= list()
		discount= list()

		ix = open_dir('exampleIndex')
		schema = ix.schema
		# Create query parser that looks through designated fields in index
		og = qparser.OrGroup.factory(0.9)
		mp = qparser.MultifieldParser(['item', 'description','picture','productType','brand','size','price','url','onsale','discount'], schema =self.ix.schema, group = og)

		# This is the user query
		#query = input("Please enter a Title, Year, Rating, IMDB tag, or some type of key word description:")
		q = mp.parse(queryEntered)
		#threshold = int(input("How many results would you like?:"))
		# Actual searcher, prints top 10 hits
		with ix.searcher() as s:
			results = s.search_page(q, page, sortedby="price")	#search page by sorting of the price tag
			print("Search Results: ")
			try:
				for i in results:
					
					#append the results
					item.append(i['item'])
					description.append(i['description'])
					picture.append(i['picture'])
					productType.append(i['productType'])
					brand.append(i['brand'])
					size.append(i['size'])
					price.append(i['price'])
					url.append(i['url'])
					onsale.append(i['onsale'])
					discount.append(i['discount'])

			except IndexError:							#if it doesnt find x number of results it catches the error 
				pass									#program goes into the infinite while loop for another query
		return  item, description, picture, productType, brand, size, price, url, onsale, discount, page, len(results)


if __name__ == '__main__':
	
	global mysearch
	mysearch = wooshSearch()
	
	#mysearch.index_search()
	mysearch.index()
	
	app.run(debug=True, use_reloader =False)

	

	


	
	
	