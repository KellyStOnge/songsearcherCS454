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




app = Flask('__name__')


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

	
	artist_id, artist, album, album_release,track, artist_image, album_art, preview_link, link_tosong, lyrics, artist_genres, date_released ,ra1,ra2,ra3,ra4,ra5,ra1l,ra2l,ra3l,ra4l,ra5l, page,  Results = mysearch.index_search(keywordquery,page+1)
	
	pag = math.ceil(Results/10) # passing the number of results so that the #number of pages shows 

	if page == pag: #
		page -=1	# SO IT DOESNT PASS THE TOTAL NUMBER OF PAGES
		return render_template('results.html', query=keywordquery, len = len(artist), pag = pag , page = page, artist_id = artist_id, artist= artist, album =album, album_release =album_release, track = track, artist_image= artist_image, album_art = album_art, 
		 preview_link = preview_link, link_tosong =link_tosong, lyrics =lyrics, artist_genres =artist_genres,date_released =date_released,ra1=ra1,ra2=ra2,ra3=ra3,ra4=ra4,ra5=ra5,ra1l=ra1l,
		 ra2l=ra2l,ra3l=ra3l,ra4l=ra4l,ra5l=ra5l)
	else:
		return render_template('results.html', query=keywordquery, len = len(artist), pag = pag , page = page, artist_id = artist_id, artist= artist, album =album, album_release =album_release, track = track, artist_image= artist_image, album_art = album_art, 
		 preview_link = preview_link, link_tosong =link_tosong, lyrics =lyrics, artist_genres =artist_genres,date_released =date_released,ra1=ra1,ra2=ra2,ra3=ra3,ra4=ra4,ra5=ra5,ra1l=ra1l,
		 ra2l=ra2l,ra3l=ra3l,ra4l=ra4l,ra5l=ra5l)


@app.route('/previous/<q>/<p>' , methods=["GET", "POST"])
def previous(q,p):
	global mysearch
	data = request.form

	
	keywordquery = q
	int(p)

	page = int(p)


	if page <=1:
		page==2
		
		artist_id, artist, album, album_release,track, artist_image, album_art, preview_link, link_tosong, lyrics, artist_genres, date_released ,ra1,ra2,ra3,ra4,ra5,ra1l,ra2l,ra3l,ra4l,ra5l, page,  Results = mysearch.index_search(keywordquery,page)
		
		pag = math.ceil(Results/10)

		return render_template('results.html', query=keywordquery, len = len(artist), pag = pag , page = page, artist_id = artist_id, artist= artist, album =album, album_release =album_release, track = track, artist_image= artist_image, album_art = album_art, 
		 preview_link = preview_link, link_tosong =link_tosong, lyrics =lyrics, artist_genres =artist_genres,date_released =date_released,ra1=ra1,ra2=ra2,ra3=ra3,ra4=ra4,ra5=ra5,ra1l=ra1l,
		 ra2l=ra2l,ra3l=ra3l,ra4l=ra4l,ra5l=ra5l)
		
	else:
		print(page)
		artist_id, artist, album, album_release,track, artist_image, album_art, preview_link, link_tosong, lyrics, artist_genres, date_released ,ra1,ra2,ra3,ra4,ra5,ra1l,ra2l,ra3l,ra4l,ra5l, page,  Results = mysearch.index_search(keywordquery,page-1)

		pag = math.ceil(Results/10)

		return render_template('results.html', query=keywordquery, len = len(artist), pag = pag , page = page, artist_id = artist_id, artist= artist, album =album, album_release =album_release, track = track, artist_image= artist_image, album_art = album_art, 
		 preview_link = preview_link, link_tosong =link_tosong, lyrics =lyrics, artist_genres =artist_genres,date_released =date_released,ra1=ra1,ra2=ra2,ra3=ra3,ra4=ra4,ra5=ra5,ra1l=ra1l,
		 ra2l=ra2l,ra3l=ra3l,ra4l=ra4l,ra5l=ra5l)


@app.route('/results/', methods=['GET', 'POST'])
def results():
	global mysearch
	page = 1
	if request.method == 'POST':
		data = request.form

	else:
		data = request.args

	keywordquery = data.get('searchterm')
	

	artist_id, artist, album, album_release,track, artist_image, album_art, preview_link, link_tosong, lyrics, artist_genres, date_released,ra1,ra2,ra3,ra4,ra5,ra1l,ra2l,ra3l,ra4l,ra5l, page,  Results = mysearch.index_search(keywordquery,page)
	
	pag = math.ceil(Results/10)

	if Results == 0:
		flash("Not in the search, try again")
		return render_template('welcome_page.html')
	else:
		return render_template('results.html', query=keywordquery, len = len(artist), pag = pag , page = page, artist_id = artist_id, artist= artist, album =album, album_release =album_release, track = track, artist_image= artist_image, album_art = album_art, 
		 preview_link = preview_link, link_tosong =link_tosong, lyrics =lyrics, artist_genres =artist_genres,date_released =date_released,ra1=ra1,ra2=ra2,ra3=ra3,ra4=ra4,ra5=ra5,ra1l=ra1l,
		 ra2l=ra2l,ra3l=ra3l,ra4l=ra4l,ra5l=ra5l)




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

			data = pd.read_csv("finalwlyricsexample.csv")

			related_keys = data['related_artists'].map(eval)

			print(len(related_keys))

		schema = Schema(artist_id=TEXT(stored=True), artist=TEXT(stored=True), album=TEXT(stored = True),album_release=TEXT(stored = True),track =TEXT(stored = True),artist_image=TEXT(stored = True),album_art=TEXT(stored = True),
			preview_link=TEXT(sortable=True),link_tosong=TEXT(stored = True),lyrics=TEXT(stored = True),artist_genres=TEXT(stored = True),date_released=TEXT(stored = True),
			ra1=TEXT(sortable=True),ra2=TEXT(sortable=True),ra3=TEXT(sortable=True),ra4=TEXT(sortable=True),ra5=TEXT(sortable=True),ra1l=TEXT(sortable=True),ra2l=TEXT(sortable=True),ra3l=TEXT(sortable=True),ra4l=TEXT(sortable=True),
			ra5l=TEXT(sortable=True))
		
		ix = create_in('exampleIndex', schema)
		
		# Imports stories from pandas df
		

		print (len(list(df)))
		
		for i in range(len(list(df))-1):		#go the length of the index

			rk = related_keys[i]

			keys  = []
			items = []
			for key,item in rk.items():
				keys.append([key])
				items.append([item])

			

			for val in list(df[i+1]):

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
						   artist_genres = (val[11]),
						   date_released = (val[12]),
						   ra1 =(keys[0]),
						   ra2 =(keys[1]),
						   ra3 =(keys[2]),
						   ra4 =(keys[3]),
						   ra5 =(keys[4]),
						   ra1l =(items[0]),
						   ra2l =(items[1]),
						   ra3l =(items[2]),
						   ra4l =(items[3]),
						   ra5l =(items[4]))

				writer.commit()
				self.ix = ix

				print ("writing doc",i+1)

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
		artist_genres= list()
		date_released= list()
		ra1 =list()
		ra2 =list()
		ra3 =list()
		ra4 =list()
		ra5 =list()
		ra1l =list()
		ra2l =list()
		ra3l =list()
		ra4l =list()
		ra5l =list()




		ix = open_dir('exampleIndex')
		schema = ix.schema
		# Create query parser that looks through designated fields in index
		og = qparser.OrGroup.factory(0.9)
		mp = qparser.MultifieldParser(['artist_id', 'artist','album','album_release','track','artist_image','album_art','preview_link','link_tosong','lyrics','related_artists','artist_genres','date_released','ra1',
			'ra2','ra3','ra4','ra5','ra1l','ra2l','ra3l','ra4l','ra5l'], schema =self.ix.schema, group = og)


		q = mp.parse(queryEntered)
		#threshold = int(input("How many results would you like?:"))
		# Actual searcher, prints top 10 hits
		with ix.searcher() as s:
			results = s.search_page(q, page)	#user threshold
			print("Search Results: ")
			try:
				for i in results:


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
					
					artist_genres.append(i['artist_genres'])
					date_released.append(i['date_released'])
					ra1.append(i['ra1'])
					ra2.append(i['ra2'])
					ra3.append(i['ra3'])
					ra4.append(i['ra4'])
					ra4.append(i['ra5'])
					ra1l.append(i['ra1l'])
					ra2l.append(i['ra2l'])
					ra3l.append(i['ra3l'])
					ra4l.append(i['ra4l'])
					ra5l.append(i['ra5l'])
							

			except IndexError:							#if it doesnt find x number of results it catches the error 
				pass									#program goes into the infinite while loop for another query
		return  artist_id, artist, album, album_release,track, artist_image, album_art, preview_link, link_tosong, lyrics, artist_genres, date_released ,ra1,ra2,ra3,ra4,ra5,ra1l,ra2l,ra3l,ra4l,ra5l, page, len(results)



if __name__ == '__main__':
	
	global mysearch
	mysearch = wooshSearch()
	
	#mysearch.index_search()
	mysearch.index()
	
	app.run(debug=True, use_reloader =False)

	

	


	
	
	