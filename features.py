from __future__ import print_function    # (at top of module)
from spotipy.oauth2 import SpotifyClientCredentials

import spotipy
import spotipy.util as util
import requests
import json
import pandas as pd
import csv

#Work Search
searchname = pd.read_csv(‘insert path.csv', encoding='cp1252') 

#Give spotify API key credentials - insert ID and Client Secret here
client_credentials_manager = SpotifyClientCredentials(client_id='insert id', client_secret='insert secret')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=False

#Pull song features from API

songs = []
name = []
for row in searchname.search_name:

    results = sp.search(q=row, limit=1)
    tids = []
        
    for i, t in enumerate(results['tracks']['items']):
        tids.append(t['uri'])
        name.append({'Search': row, 'Name': t['name'], 'id': t['id'], 'Popularity': t['popularity'], 'Artist': t['artists']})
        features = sp.audio_features(tids)
        
        for feature in features:
            songs.append(feature)


#convert JSON object into the dataframe
def make_audio_features_df(features):
    audio_features_df = pd.DataFrame(columns = features[0])
    for i in features:
        audio_features_df = audio_features_df.append(i, ignore_index=True)
return audio_features_df

audio_features_df = make_audio_features_df(songs)

spotify_features = pd.DataFrame(name)


spotify_features.merge(audio_features_df, on='id').to_csv('SPOTIFY API RESULTS.csv', index=False)
            

