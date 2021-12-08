import requests
from bs4 import BeautifulSoup
import csv
from csv import DictReader
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data
import json
import pandas as pd
import time 
import os.path
import numpy as np
from lyricsgenius import Genius


client_id = '067cc1d0NOSOUPFORYOU788b98cb11' #linden find a key
client_secret = '80176a5bf9NOSOUPFORYOUb96a5888e3' #Linden find a key via spotipy api
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager) #spotify object to access API

def related_artists(name):
	artist_results = sp.search(q='artist:' + name, type='artist')

	items = artist_results['artists']['items']
	if len(items) > 0:
		artist = items[0]


	artist_uri = artist['uri']


	relatedDict = {}

#print(artist_info)

	related = sp.artist_related_artists(artist_uri)


	noa = len(related['artists'])

	for i in range(1,noa):
	#print(related['artists'][i]['name'],"-", related['artists'][i]['uri'])

		relatedDict[related['artists'][i]['name']] = related['artists'][i]['uri']


	return relatedDict


