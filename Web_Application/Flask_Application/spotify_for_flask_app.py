# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 14:32:16 2021
@author: Luke Hillery
"""

import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
import os
import time
from datetime import datetime
import requests
import statistics
from twilio.rest import Client
import config

# Create a spotify authorization object ie trigger spotify permission pop up
def createSpotify():
    # Spotify Authorization #
    token = util.prompt_for_user_token(
        username=config.username,
        scope="playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative user-read-recently-played user-top-read user-read-playback-position app-remote-control streaming user-library-modify user-library-read user-read-playback-state user-modify-playback-state user-read-currently-playing",
        client_id=config.SPOTIPY_CLIENT_ID,
        client_secret=config.SPOTIPY_CLIENT_SECRET,
        redirect_uri=config.SPOTIPY_REDIRECT_URI
        )
    # Create spotify object with permissions
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    #creates cache file config.cpython-39.pyc with auth token and refresh token inside
    return sp


if __name__ == "__main__":
    createSpotify()

'''
# Create model of user based on their top songs
def getUserMood(username,sp):
    return

def startAnalysis(username,sp,my_number,emergency_number,min_valence):
    # username = user's your_username
    # sp = spotifyObject with permissions
    # my_number = phone number for the user
    # emergency_number = phone number for chosen emergency contact
    # min_valence = the trigger value for session mood
    return
'''
