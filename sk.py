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


genius = Genius('IFhK-56V9SWfo-XcvYNOSOUP4Uqa_SYCMVxXJzea9VNYcXti7gT') #destroyed keys for showing code on GITHUB

sleep_min = 2
sleep_max = 5
start_time = time.time()
request_count = 0


#Scrapes 1000 popular artists from song kick

i = 1

file = open('popular_artists.csv', 'w')
writer = csv.writer(file)

writer.writerow(['Artist'])

for i in range(1,6):
	URL = "https://www.songkick.com/leaderboards/popular_artists?page="+str(i)
	page = requests.get(URL)
	soup = BeautifulSoup(page.content)
	results = soup.find_all("td",class_="name")
	for x in results:
		name = x.find("a").text
		writer.writerow([name])


file.close()


#SPOTIFY AUTHORIZATION

client_id = '067cc1d0e5ff4c7NOSOUP4Uc7b98cb11'
client_secret = '80176a5bf92NOSOUP4Uc0b96a5888e3'
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
		artist_results = sp.search(q='artist:' + name, type='artist') # searches for artist in the popular artist list 

		items = artist_results['artists']['items'] #stores the query format into items
		
		if len(items) > 0: #returns firsrt result / not always the best but gets it right 95% of the time
			artist = items[0]


		artist_info = result['tracks']['items'][0]['artists']


		###########################

		
		
		artist_uri = artist['uri'] #stores the URI for the artist this is important because its the info for everything


		relArtist = related_artists(artist['name']) # storing related artist in this part of the for loop

		artist_genres = artist['genres']	# artist genres


		

		results = sp.artist_albums(artist_uri, album_type='album') # this is the individual albums of an artist
		albums = results['items']
		while results['next']:
			results = sp.next(results)
			albums.extend(results['items'])

		for album in albums:


			tracks = sp.album_tracks(album['uri']) # this gets all the tracks

			date_released = album["release_date"] # the release date for the album
			

			for track in range(len(tracks['items'])):


				try:
					song = genius.search_song(tracks['items'][track]['name'], album['artists'][0]['name']) # this uses the genius (lyrics) api
				except requests.exceptions.Timeout:

					print("retrying because of Timeout") #there were a lot of time outs this try except makes sure that the for loop covers that song
					track -=2

					time.sleep(10) # giving it 10 seconds to retry
					break	



				if song == None:
					lyrics = None
				else:
					lyrics = song.lyrics.strip() # strips the lyrics if there is any

				fields = ['artist_id','artist','album','album_release','track','artist_image','album_art','preview_link','link_tosong','lyrics',
				'related_artists', 'artist_genres','date_released']

				data = [album['artists'][0]['id'],album['artists'][0]['name'],album['name'],album['release_date'],tracks['items'][track]['name'],artist['images'][0]['url'],album['images'][0]['url'],tracks['items'][track]['preview_url'],tracks['items'][track]['uri'],lyrics,relArtist,artist_genres,date_released]

				print(data)

				print("\n\n\n\n\n")

				with open(final, 'a') as f: # writes all fields and other needed information to the csv 
					writer = csv.writer(f)
					writer.writerow(data)

				
		
print("ITS done!!")



