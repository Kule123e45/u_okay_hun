# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 14:32:16 2021

@author: higor
"""
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import os
import time
from datetime import datetime
import requests

#import pandas as pd



os.environ["username"] = config.username
scope = "playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative user-read-recently-played user-top-read user-read-playback-position app-remote-control streaming user-library-modify user-library-read user-read-playback-state user-modify-playback-state user-read-currently-playing"
os.environ["SPOTIPY_CLIENT_ID"] = config.SPOTIPY_CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = config.SPOTIPY_CLIENT_SECRET
os.environ["SPOTIPY_REDIRECT_URI"] = config.SPOTIPY_REDIRECT_URI


#sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# =============================================================================
# getTrackIDs - Takes a user and playlist id and extracts the track_id for
#               each track in that playlist.
# =============================================================================
def getTrackIDs(user, playlist_id,sp):
    ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids

#To call function:
#ids = getTrackIDs('angelicadietzel', '4R0BZVh27NUJhHGLNitU08')
#print(ids)
# =============================================================================

# =============================================================================
# getTrackFeatures - Takes a track id and creates a list of the metadata and
#                    music features of the track.
# =============================================================================
def getTrackFeatures(id,sp):
  meta = sp.track(id)
  features = sp.audio_features(id)
  # meta data
  name = meta['name']
  album = meta['album']['name']
  artist = meta['album']['artists'][0]['name']
  release_date = meta['album']['release_date']
  length = meta['duration_ms']
  popularity = meta['popularity']
  # track features
  acousticness = features[0]['acousticness']
  danceability = features[0]['danceability']
  energy = features[0]['energy']
  instrumentalness = features[0]['instrumentalness']
  liveness = features[0]['liveness']
  loudness = features[0]['loudness']
  speechiness = features[0]['speechiness']
  tempo = features[0]['tempo']
  time_signature = features[0]['time_signature']
  valence = features[0]['valence'] # a proxy for 'mood' or 'positivity' of track

  # Possible output formats (return as appropriate)
  track = [name, album, artist, release_date, length, popularity, danceability,
            acousticness, energy, instrumentalness, liveness, loudness,
            speechiness, tempo, valence, time_signature]
  track_features = [danceability, acousticness, energy, instrumentalness,
                    liveness, loudness, speechiness, tempo, valence]
  track_mood = [valence]
  track_mood_ext = [valence, energy, danceability, tempo]
  return track_mood_ext

#To call the function:
#tracks = []
#for i in range(len(ids)):
#  time.sleep(.5)
#  track = getTrackFeatures(ids[i])
#  tracks.append(track)
# =============================================================================

# =============================================================================
# getTrackMood - Takes a track id and returns its valence
# =============================================================================
def getTrackMood(id):
  features = sp.audio_features(id)
  valence = features[0]['valence']

  track_mood = [valence]
  return track_mood
#==============================================================================

#to be developed.........................


# =============================================================================
# getUserMoodFromTop - Takes a user id and returns their avg playback mood
#                      based on their top tracks according to SpotifyAPI
# =============================================================================
'''
def getUserMoodFromTop(user):
    return
'''
# =============================================================================

# =============================================================================
# getUserCurrentMood - Takes a user id and returns the avg mood of the tracks
#                      played in the last hour
# =============================================================================
'''
def getUserCurrentMood(user):
    return
'''
# =============================================================================

# =============================================================================
# getLocalMood - Uses fycharts API to pull local (GB) top 200 songs and
#                determine their mood for comparison to the user
# =============================================================================
'''
def getLocalMood():
    local_mood = [valence, energy, danceability, tempo]
    return local_mood
'''
# =============================================================================

# =============================================================================
# getGlobalMood - Uses fycharts API to pull global top 200 songs and
#                determine their mood for comparison to the user
# =============================================================================
'''
def getGlobalMood():
    global_mood = [valence, energy, danceability, tempo]
    return global_mood
'''
# =============================================================================


# =============================================================================
# Spotify_API - Takes full authentication dataset to return currently playing
#               track, publishing track and playback data to thingspeak
# =============================================================================
def Spotify_API(your_username, scope, client_id, client_secret, redirect_uri):
    token = util.prompt_for_user_token(
        username=your_username,
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri)

    # Create spotify object with permissions
    #spotifyObject = spotipy.Spotify(auth=token) #Leah's one
    spotifyObject = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # Get current playing track
    devices = spotifyObject.current_user_playing_track()
    trackplaying = devices['is_playing']


    if trackplaying:
        # Connvert UNIX time stamp to YMDHMS
        time = devices['timestamp']/1E3
        timedate = datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')
        #print(devices)
        name = devices['item']['name'] #song name
        url = devices['item']['external_urls']['spotify'] # song url
        artist = devices['item']['album']['artists'][0]['name'] #artist name
        artist2 = devices['item']['album']['artists'][0]['uri']
        album = devices['item']['album']['name'] #album name
        duration = devices['item']['duration_ms'] #song duration
        album_image_url = devices['item']['album']['images'][0]['url'] #album image url
        #T/F track is playing
        trackid = devices['item']['uri'] #Spotify track ID

        artists = spotifyObject.artist(artist2)
        genres = artists['genres']
        #print(genres)
        analysis = spotifyObject.audio_features(trackid);
        #print(str(trackplaying))
        if genres == []:
            return [analysis[0]['valence'], timedate, name, artist, album, trackid, 'No genre found', trackplaying, analysis[0]['tempo'], analysis[0]['danceability'],
                    analysis[0]['energy']]
        else:
            return [analysis[0]['valence'], timedate, name, artist, album, trackid, genres[0],trackplaying, analysis[0]['tempo'], analysis[0]['danceability'],
                    analysis[0]['energy']]
    else:
        return ['N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A',trackplaying, 'N/A', 'N/A','N/A']





# =============================================================================



try:
    while True:
        try:
            valence, timedate, name, artist, album, trackid, genre ,trackplaying, tempo, danceability, energy = Spotify_API(config.username,scope,config.SPOTIPY_CLIENT_ID,config.SPOTIPY_CLIENT_SECRET,config.SPOTIFY_REDIRECT_URI)
            if trackplaying:
                print("Now playing: {} by {}. How u feelin hun?...".format(name, artist))
                trackplaying_binary = 1
                RequestToThingspeak = 'https://api.thingspeak.com/update?api_key='+config.THINGSPEAK_CHANNEL_API_1+'&field1='+str(trackplaying_binary)+'&field2='+str(genre)+'&field3='+str(tempo)+'&field4='+str(danceability)+'&field5='+str(valence)+'&field6='+str(energy)
                request = requests.get(RequestToThingspeak)
                print('**Posted track data to thingspeak**')
                time.sleep(120)
            else:
                print('Nothing playing...')
                trackplaying_binary = 0
                emptyRequestToThingspeak = 'https://api.thingspeak.com/update?api_key='+config.THINGSPEAK_CHANNEL_API_1+'&field1=0&field2=N/A&field3=N/A&field4=N/A&field5=N/A&field6=N/A'
                request = requests.get(emptyRequestToThingspeak)
                print('**Posted empty dataset to thingspeak**')
                time.sleep(120)
        except TypeError:
            trackplaying_binary = 0
            emptyRequestToThingspeak = 'https://api.thingspeak.com/update?api_key='+config.THINGSPEAK_CHANNEL_API_1+'&field1=0&field2=N/A&field3=N/A&field4=N/A&field5=N/A&field6=N/A'
            request = requests.get(emptyRequestToThingspeak)
            print('TypeError occured, empty dataset posted to Thingspeak')
            time.sleep(120)

except KeyboardInterrupt:
    pass



