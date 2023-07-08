import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
import csv

# replace with your own client ID and client secret key
client_id = ''
client_secret = ''

# authenticate with the Spotify Web API
try:
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
except Exception as e:
    print(f"Failed to authenticate with the Spotify API: {e}")
    exit()

# get a list of random track IDs from 2021
try:
    results = sp.search(q='year:2021-2022', type='track', limit=50)
    tracks = results['tracks']['items']
    while len(tracks) < 100:
        results = sp.search(q='year:2021-2022', type='track', limit=50, offset=len(tracks))
        tracks += results['tracks']['items']
    random.shuffle(tracks)
    track_ids = [track['id'] for track in tracks[:20]]
except Exception as e:
    print(f"Failed to get track IDs: {e}")
    exit()

# get audio features and popularity for the random tracks
try:
    audio_features = sp.audio_features(track_ids)
    tracks = sp.tracks(track_ids)['tracks']
except Exception as e:
    print(f"Failed to get audio features and track details: {e}")
    exit()

# create a list of dictionaries for the CSV file
csv_data = []
for features, track in zip(audio_features, tracks):
    row = {
        'acousticness': features['acousticness'],
        'analysis_url': features['analysis_url'],
        'danceability': features['danceability'],
        'duration_ms': features['duration_ms'],
        'energy': features['energy'],
        'id': features['id'],
        'instrumentalness': features['instrumentalness'],
        'key': features['key'],
        'liveness': features['liveness'],
        'loudness': features['loudness'],
        'mode': features['mode'],
        'speechiness': features['speechiness'],
        'tempo': features['tempo'],
        'time_signature': features['time_signature'],
        'track_href': features['track_href'],
        'type': features['type'],
        'uri': features['uri'],
        'valence': features['valence'],
        'popularity': track['popularity'],
        'song_name': track['name'],
        'artist_name': track['artists'][0]['name'],
        'year': track['album']['release_date'][:4] # get the year from the album release date
    }
    csv_data.append(row)

# write the CSV file
try:
    with open('audio_features.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['acousticness', 'analysis_url', 'danceability', 'duration_ms', 'energy', 'id', 'instrumentalness',
                      'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'track_href',
                      'type', 'uri', 'valence', 'popularity', 'song_name', 'artist_name', 'year']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)
except Exception as e:
    print(f"Failed to write CSV file: {e}")
    exit()
