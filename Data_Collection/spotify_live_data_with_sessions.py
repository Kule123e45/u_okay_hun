# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 14:32:16 2021
@author: Luke Hillery

Credit to
"""

# This script record live spotify user data to a Thingspeak data channel
# See supporting documentation for more information on this project
# Effort has been taken to remove sensitive and confidental information

# import necessary packages
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import os
import time
from datetime import datetime
import requests
import statistics
import config

# import sensitive variables from config.py file
os.environ["username"] = config.username
scope = "playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative user-read-recently-played user-top-read user-read-playback-position app-remote-control streaming user-library-modify user-library-read user-read-playback-state user-modify-playback-state user-read-currently-playing"
os.environ["SPOTIPY_CLIENT_ID"] = config.SPOTIPY_CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = config.SPOTIPY_CLIENT_SECRET
os.environ["SPOTIPY_REDIRECT_URI"] = config.SPOTIPY_REDIRECT_URI
#os.environ["OAUTH_AUTHORIZE_URL"] = "https://accounts.spotify.com/authorize"
#os.environ["OAUTH_TOKEN_URL"] = "https://accounts.spotify.com/api/token"

# =============================================================================
# getTrackIDs - Takes a user and playlist id and extracts the track_id for
#               each track in that playlist. Authorised spotify user object
#               (sp) must be passed.
# =============================================================================
def getTrackIDs(user, playlist_id,sp):
    ids = []
    playlist = sp.user_playlist(user, playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        ids.append(track['id'])
    return ids
# =============================================================================
# getTrackFeatures - Takes a track id and creates a list of the metadata and
#                    music features of the track. Authorised spotify user object
#                    (sp) must be passed.
# =============================================================================
def getTrackFeatures(id,sp):
  meta = sp.track(id)
  features = sp.audio_features(id)
  # meta data
  name = meta['name']
  album = meta['album']['name']
  artist = meta['album']['artists'][0]['name']
  #release_date = meta['album']['release_date']
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
  #track = [name, album, artist, release_date, length, popularity, danceability,
    #        acousticness, energy, instrumentalness, liveness, loudness,
    #        speechiness, tempo, valence, time_signature]
  #track_features = [danceability, acousticness, energy, instrumentalness,
    #                liveness, loudness, speechiness, tempo, valence]
  #track_mood = [valence]
  track_mood_ext = [valence, energy, danceability, tempo]
  return track_mood_ext
# =============================================================================
# Spotify_API - Takes full authentication dataset to return currently playing
#               track, publishing track and playback data to thingspeak
# =============================================================================
def Spotify_API(your_username, scope, client_id, client_secret, redirect_uri):
    # generate a token using spotify authorisation credentials
    token = util.prompt_for_user_token(
        username=your_username,
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri)

    # Create spotifyObject with permissions,auth_manager handles token refresh
    spotifyObject = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    # Get current playing track
    devices = spotifyObject.current_user_playing_track()
    trackplaying = devices['is_playing']

    #T/F track is playing
    if trackplaying:
        # Connvert UNIX time stamp to YMDHMS
        time = devices['timestamp']/1E3
        timedate = datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')
        name = devices['item']['name'] #song name
        artist = devices['item']['album']['artists'][0]['name'] #artist name
        artist2 = devices['item']['album']['artists'][0]['uri']
        album = devices['item']['album']['name'] #album name
        #album_image_url = devices['item']['album']['images'][0]['url'] #album image url
        trackid = devices['item']['uri'] #Spotify track ID
        artists = spotifyObject.artist(artist2)
        genres = artists['genres']
        analysis = spotifyObject.audio_features(trackid);

        if genres == []:
            return [analysis[0]['valence'], timedate, name, artist, album, trackid, 'No genre found', trackplaying, analysis[0]['tempo'], analysis[0]['danceability'],
                    analysis[0]['energy']]
        else:
            return [analysis[0]['valence'], timedate, name, artist, album, trackid, genres[0],trackplaying, analysis[0]['tempo'], analysis[0]['danceability'],
                    analysis[0]['energy']]
    else:
        return ['N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A',trackplaying, 'N/A', 'N/A','N/A']


def Extract1st(lst):
    return [item[0] for item in lst]
def Extract2nd(lst):
    return [item[1] for item in lst]
def Extract3rd(lst):
    return [item[2] for item in lst]
def Extract4th(lst):
    return [item[3] for item in lst]

# =============================================================================



try:
    session_bucket = []
    session_bucket_size = 0
    sleep_time = 120 # time (s) between samples
    SET_BUCKET_SIZE = int(30) # number of samples in each session
    while True:
        try:
            valence, timedate, name, artist, album, trackid, genre ,trackplaying, tempo, danceability, energy = Spotify_API("Luke Hillery",scope,"3f203afa2be240ffbcaa571e12eee03e","6947e86380b949d1b5665125bf4dfd4c","http://localhost:8888/callback")
            if trackplaying:
                trackplaying_binary = 1
                RequestToThingspeak = 'https://api.thingspeak.com/update?api_key=RYJ2D37RI5EGO0MP&field1='+str(trackplaying_binary)+'&field2='+str(genre)+'&field3='+str(tempo)+'&field4='+str(danceability)+'&field5='+str(valence)+'&field6='+str(energy)
                request = requests.get(RequestToThingspeak)
                print("Now playing: {} by {}. Posted data to Thingspeak.".format(name, artist))
                if session_bucket_size < SET_BUCKET_SIZE:
                    session_bucket_size += 1
                    print('Current session dataset size: '+str(session_bucket_size))
                    session_bucket.append([tempo, danceability,valence,energy])
                else:
                    if session_bucket:
                        session_tempo = statistics.mean(Extract1st(session_bucket))
                        session_danceability = statistics.mean(Extract2nd(session_bucket))
                        session_valence = statistics.mean(Extract3rd(session_bucket))
                        session_energy = statistics.mean(Extract4th(session_bucket))
                        session_tempo_std = statistics.stdev(Extract1st(session_bucket))
                        session_danceability_std = statistics.stdev(Extract2nd(session_bucket))
                        session_valence_std = statistics.stdev(Extract3rd(session_bucket))
                        session_energy_std = statistics.stdev(Extract4th(session_bucket))
                        print('============================================')
                        print('**SESSION SUMMARY**')
                        print('Session mean valence: {:.3f}, deviation = {:.3f}'.format((session_valence),(session_valence_std)))
                        print('Session mean energy: {:.3f}, deviation = {:.3f}'.format((session_energy),(session_energy_std)))
                        print('Session mean danceability: {:.3f}, deviation = {:.3f}'.format((session_danceability),(session_danceability_std)))
                        print('Session mean tempo: {:.3f}, deviation = {:.3f}'.format((session_tempo),(session_tempo_std)))
                        SessionRequestToThingspeak = 'https://api.thingspeak.com/update?api_key=L4P6XPRO3ODASMS3&field1='+str(session_valence)+'&field2='+str(session_energy)+'&field3='+str(session_danceability)+'&field4='+str(session_tempo)
                        request = requests.get(SessionRequestToThingspeak)
                        print('============================================')
                        if len(session_bucket) < (SET_BUCKET_SIZE/2):
                            session_bucket = []
                            session_bucket_size = 0
                            print('Session dataset is less than half full. Dataset emptied.')
                        else:
                            print('Session dataset is more than half full. First half of session deleted.')
                            session_bucket = session_bucket[15:] #check this works
                            session_bucket_size = len(session_bucket)

                            #print('Half session deleted (track playing), starting new session with: '+str(session_bucket_size))
                    else:
                        print('No data in session. Nothing executed. (track playing)')
                        session_bucket_size = 0

                    #post session data
                time.sleep(sleep_time)


            else:
                trackplaying_binary = 0
                emptyRequestToThingspeak = 'https://api.thingspeak.com/update?api_key=RYJ2D37RI5EGO0MP&field1=0&field2=N/A&field3=N/A&field4=N/A&field5=N/A&field6=N/A'
                request = requests.get(emptyRequestToThingspeak)
                print('No track currently playing. Empty dataset posted to Thingspeak.')
                if session_bucket_size < SET_BUCKET_SIZE:
                    session_bucket_size += 1
                    print('Session bucket (no track playing): '+str(session_bucket_size))
                else:
                    if session_bucket:
                        session_tempo = statistics.mean(Extract1st(session_bucket))
                        session_danceability = statistics.mean(Extract2nd(session_bucket))
                        session_valence = statistics.mean(Extract3rd(session_bucket))
                        session_energy = statistics.mean(Extract4th(session_bucket))

                        session_tempo_std = statistics.stdev(Extract1st(session_bucket))
                        session_danceability_std = statistics.stdev(Extract2nd(session_bucket))
                        session_valence_std = statistics.stdev(Extract3rd(session_bucket))
                        session_energy_std = statistics.stdev(Extract4th(session_bucket))
                        print('============================================')
                        print('**SESSION SUMMARY**')
                        print('Session mean valence: {:.3f}, deviation = {:.3f}'.format((session_valence),(session_valence_std)))
                        print('Session mean energy: {:.3f}, deviation = {:.3f}'.format((session_energy),(session_energy_std)))
                        print('Session mean danceability: {:.3f}, deviation = {:.3f}'.format((session_danceability),(session_danceability_std)))
                        print('Session mean tempo: {:.3f}, deviation = {:.3f}'.format((session_tempo),(session_tempo_std)))
                        print('============================================')
                        if len(session_bucket) < (SET_BUCKET_SIZE/2):
                            session_bucket = []
                            session_bucket_size = 0
                            print('Bucket less than half full, emptied bucket.')
                        else:
                            print('Session dataset is more than half full. First half of session deleted.')
                            session_bucket = session_bucket[15:] #check this works
                            session_bucket_size = len(session_bucket)

                    else:
                        print('No data in session. Nothing executed. (no track playing)')
                        session_bucket_size = 0
                time.sleep(sleep_time)


        except TypeError:
            trackplaying_binary = 0
            emptyRequestToThingspeak = 'https://api.thingspeak.com/update?api_key=RYJ2D37RI5EGO0MP&field1=0&field2=N/A&field3=N/A&field4=N/A&field5=N/A&field6=N/A'
            request = requests.get(emptyRequestToThingspeak)
            print('TypeError occured, empty dataset posted to Thingspeak')
            if session_bucket_size < SET_BUCKET_SIZE:
                session_bucket_size += 1
                print('Session bucket (TypeError): '+str(session_bucket_size))
            else:
                if session_bucket:
                    session_tempo = statistics.mean(Extract1st(session_bucket))
                    session_danceability = statistics.mean(Extract2nd(session_bucket))
                    session_valence = statistics.mean(Extract3rd(session_bucket))
                    session_energy = statistics.mean(Extract4th(session_bucket))

                    session_tempo_std = statistics.stdev(Extract1st(session_bucket))
                    session_danceability_std = statistics.stdev(Extract2nd(session_bucket))
                    session_valence_std = statistics.stdev(Extract3rd(session_bucket))
                    session_energy_std = statistics.stdev(Extract4th(session_bucket))
                    print('============================================')
                    print('           **SESSION SUMMARY**')
                    print('Session mean valence: {:.3f}, deviation = {:.3f}'.format((session_valence),(session_valence_std)))
                    print('Session mean energy: {:.3f}, deviation = {:.3f}'.format((session_energy),(session_energy_std)))
                    print('Session mean danceability: {:.3f}, deviation = {:.3f}'.format((session_danceability),(session_danceability_std)))
                    print('Session mean tempo: {:.3f}, deviation = {:.3f}'.format((session_tempo),(session_tempo_std)))
                    print('============================================')
                    if len(session_bucket) < (SET_BUCKET_SIZE/2):
                        session_bucket = []
                        session_bucket_size = 0
                        print('Bucket less than half full, emptied bucket.')
                    else:
                        session_bucket = session_bucket[15:] #check this works
                        session_bucket_size = len(session_bucket)
                        print('Session dataset is more than half full. First half of session deleted.')

                        #print('Half session deleted (track playing), starting new session with: '+str(session_bucket_size))
                else:
                    print('No data in session. Nothing executed. (TypeError)')
                    session_bucket_size = 0

            time.sleep(sleep_time)

except KeyboardInterrupt:
    pass
