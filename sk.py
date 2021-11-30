import requests
from bs4 import BeautifulSoup
import csv
from csv import DictReader
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data
import json
import pandas as pd
import time
import related
from related import related_artists
import os.path
import numpy as np
from lyricsgenius import Genius


genius = Genius('IFhK-56V9SWQbSfo-XcvYwtAQOMK_ps0pL0U91fqa_SYCMVxXJzea9VNYcXti7gT')

sleep_min = 2
sleep_max = 5
start_time = time.time()
request_count = 0


#Scrapes 1000 popular artists from song kick

i = 1

#file = open('popular_artists.csv', 'w')
#writer = csv.writer(file)

#writer.writerow(['Artist'])

#for i in range(1,6):
	#URL = "https://www.songkick.com/leaderboards/popular_artists?page="+str(i)
	#page = requests.get(URL)
	#soup = BeautifulSoup(page.content)
	#results = soup.find_all("td",class_="name")
	#for x in results:
		#name = x.find("a").text
		#writer.writerow([name])


#file.close()

client_id = '067cc1d0e5ff4c71b2310c788b98cb11'
client_secret = '80176a5bf922484dbe69c0b96a5888e3'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API

file1 =open('spotipy_artists.csv','w')

csv_artist_columns = ['id','name','uri','type','href','spotify','external_urls']
csv_artist_file = "artistSpotify.csv"
csv_artist_albums ="artistsalbums.csv"
csv_artist_albums_fields =['name', 'uri']

final ="finalwlyrics.csv"




with open('popular_artists.csv','r') as read_obj:
	csv_dreader = DictReader(read_obj)
	for row in csv_dreader:
		name = row['Artist'] #chosen artist
		result = sp.search(name) #search query
		artist_results = sp.search(q='artist:' + name, type='artist')

		items = artist_results['artists']['items']
		if len(items) > 0:
			artist = items[0]
			#print(artist['name'], artist['images'][0]['url'])

		artist_info = result['tracks']['items'][0]['artists']

		#print(artist['images'][0]['url'])

		###########################

		
		
		artist_uri = artist['uri']


		relArtist = related_artists(artist['name'])

		artist_genres = artist['genres']


		

		results = sp.artist_albums(artist_uri, album_type='album')
		albums = results['items']
		while results['next']:
			results = sp.next(results)
			albums.extend(results['items'])

		for album in albums:
			#print(album['name'])
			#print(album['uri'])
			#print(album['artists'][0]['name'], album['artists'][0]['uri'],album['name'],album['uri'],album['images'][0]['url'])
			#print(album)

			tracks = sp.album_tracks(album['uri'])

			date_released = album["release_date"]

			#song = genius.search_song(song, album['artists'][0]['name'])
			

			for track in range(len(tracks['items'])):
				#print(album['artists'][0]['name']," - " , tracks['items'][track]['name'])

				#print(tracks['items'][track]['uri'])

				try:
					song = genius.search_song(tracks['items'][track]['name'], album['artists'][0]['name'])
				except requests.exceptions.Timeout:

					print("retrying because of Timeout")
					track -=1

					time.sleep(10)
					break	



				if song == None:
					lyrics = None
				else:
					lyrics = song.lyrics.strip()

				fields = ['artist_id','artist','album','album_release','track','artist_image','album_art','preview_link','link_tosong','lyrics',
				'related_artists', 'artist_genres','date_released']

				data = [album['artists'][0]['id'],album['artists'][0]['name'],album['name'],album['release_date'],tracks['items'][track]['name'],artist['images'][0]['url'],album['images'][0]['url'],tracks['items'][track]['preview_url'],tracks['items'][track]['uri'],lyrics,relArtist,artist_genres,date_released]

				print(data)

				print("\n\n\n\n\n")

				with open(final, 'a') as f:
					writer = csv.writer(f)
					#writer.writerow(fields)
					writer.writerow(data)

				


		
print("ITS done!!")



#GENIUS WXr3SFXrdrlVSsy6oxlE2kwEpwxtN5y1VDSKHTen2zRzJ_twVi16oNEt3UjhhAAH
#		ns62Pqx1n7nAqKyhjcJF0y-bYrObWqhfibogDjhqYIGufHloklFKmT3284RprGlWbnScRrkOp72YSChzLh9u2g




