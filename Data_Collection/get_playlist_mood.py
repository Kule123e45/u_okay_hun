# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 14:32:16 2021
@author: Luke Hillery
"""

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import os
import time
from datetime import datetime
import requests
import statistics
import config
#from config import username, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

os.environ["username"] = config.username
scope = "playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative user-read-recently-played user-top-read user-read-playback-position app-remote-control streaming user-library-modify user-library-read user-read-playback-state user-modify-playback-state user-read-currently-playing"
os.environ["SPOTIPY_CLIENT_ID"] = config.SPOTIPY_CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = config.SPOTIPY_CLIENT_SECRET
os.environ["SPOTIPY_REDIRECT_URI"] = config.SPOTIPY_REDIRECT_URI
#os.environ["OAUTH_AUTHORIZE_URL"] = "https://accounts.spotify.com/authorize"
#os.environ["OAUTH_TOKEN_URL"] = "https://accounts.spotify.com/api/token"


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
def get_playlist_tracks(username,playlist_id,sp):
    ids_v2 = []
    results = sp.user_playlist_tracks(username,playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    for item in tracks:
        #track = item['track']
        ids_v2.append(item['track']['id'])
    return ids_v2
    #print(tracks)
    #return tracks
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
# getPlaylistMood - Takes a playlist id and returns the avg mood of the tracks
# =============================================================================

def getPlaylistMood(user, playlist_id, your_username, scope, client_id, client_secret, redirect_uri):

    token = util.prompt_for_user_token(
        username=your_username,
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri)

    # Create spotify object with permissions
    #spotifyObject = spotipy.Spotify(auth=token) #Leah's one
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    #playlist_tracks = getTrackIDs(user, playlist_id,sp)
    #print(playlist_tracks)
    #tracks = []
    #for i in range(len(playlist_tracks)):
    #    track = getTrackFeatures(playlist_tracks[i],sp)
    #    tracks.append(track)

    playlist_tracks_2 = get_playlist_tracks(user,playlist_id,sp)
    #print('Length of playlist_tracks_2 response: '+str(len(playlist_tracks_2)))


    # Removes NoneType errors caused by local tracks without a Spotify ID
    while None in playlist_tracks_2:
        playlist_tracks_2.remove(None)
    #print(playlist_tracks_2)
    print('Length of playlist: '+str(len(playlist_tracks_2)))

    tracks = []
    for i in range(len(playlist_tracks_2)):
        try:
            track = getTrackFeatures(playlist_tracks_2[i],sp)
            print('Analysing track '+str(i))
            tracks.append(track)
        except TypeError:
            print('Failed to analyse track '+str(i))
            pass

    print('Tracks acquired from playlist: '+str(len(tracks)))

    #print('Tracks acquired from playlist by method 2: '+str(len(playlist_tracks_2)))
    #print(tracks[0])
    #print('DIVIDERRRR')
    print(tracks[0])


    playlist_valence_list = []
    playlist_energy_list = []
    playlist_danceability_list = []
    playlist_tempo_list = []

    for track in tracks:
        playlist_valence_list.append(track[0])
        playlist_energy_list.append(track[1])
        playlist_danceability_list.append(track[2])
        playlist_tempo_list.append(track[3])

    playlist_valence = statistics.mean(playlist_valence_list)
    playlist_energy = statistics.mean(playlist_energy_list)
    playlist_danceability = statistics.mean(playlist_danceability_list)
    playlist_tempo = statistics.mean(playlist_tempo_list)
    playlist_valence_std = statistics.stdev(playlist_valence_list)
    playlist_energy_std = statistics.stdev(playlist_energy_list)
    playlist_danceability_std = statistics.stdev(playlist_danceability_list)
    playlist_tempo_std = statistics.stdev(playlist_tempo_list)

    playlist_mood = [playlist_valence, playlist_energy, playlist_danceability, playlist_tempo]
    print('============================================')
    print('**PLAYLIST MOOD SUMMARY**')
    print('Playlist mean valence: {:.3f}, deviation = {:.3f}'.format((playlist_valence),(playlist_valence_std)))
    print('Playlist mean energy: {:.3f}, deviation = {:.3f}'.format((playlist_energy),(playlist_energy_std)))
    print('Playlist mean danceability: {:.3f}, deviation = {:.3f}'.format((playlist_danceability),(playlist_danceability_std)))
    print('Playlist mean tempo: {:.3f}, deviation = {:.3f}'.format((playlist_tempo),(playlist_tempo_std)))
    print('============================================')
    return playlist_mood

# =============================================================================

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


playlist_mood = getPlaylistMood(config.username_str, '1XdKNUPTGk025fvZPBLI2Y',config.username,scope,config.SPOTIPY_CLIENT_ID,config.SPOTIPY_CLIENT_SECRET,config.SPOTIPY_REDIRECT_URI)
print(playlist_mood)

# Popsugar's Saddest Songs Ever: 1XdKNUPTGk025fvZPBLI2Y
# Luke's music: 70G9EMkvndEq0Ay6HSMgmj
