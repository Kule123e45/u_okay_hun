# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 14:32:16 2021
@author: Luke Hillery

Credit to
"""

# shows a user's playlists (need to be authenticated via oauth)
import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import os
import time
from datetime import datetime
import requests
import config

os.environ["username"] = config.username
scope = "playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative user-read-recently-played user-top-read user-read-playback-position app-remote-control streaming user-library-modify user-library-read user-read-playback-state user-modify-playback-state user-read-currently-playing"
os.environ["SPOTIPY_CLIENT_ID"] = config.SPOTIPY_CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = config.SPOTIPY_CLIENT_SECRET
os.environ["SPOTIPY_REDIRECT_URI"] = config.SPOTIPY_REDIRECT_URI

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
            track['name']))


def getPlaylistMood(username, your_username, scope, client_id, client_secret, redirect_uri):

    token = util.prompt_for_user_token(
        username=your_username,
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri)

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['owner']['id'] == username:
            print()
            print(playlist['name'])
            print ('  total tracks', playlist['tracks']['total'])
            results = sp.playlist(playlist['id'],
                fields="tracks,next")
            tracks = results['tracks']
            show_tracks(tracks)
            while tracks['next']:
                print(playlist['id'])
                tracks = sp.next(tracks)
                show_tracks(tracks)
    return tracks



playlists = getPlaylistMood(config.username_str,config.username_str,scope,config.SPOTIPY_CLIENT_ID,config.SPOTIPY_CLIENT_SECRET,config.SPOTIPY_REDIRECT_URI)


#Luke's Music Playlist id: 70G9EMkvndEq0Ay6HSMgmj
