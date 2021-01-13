from fycharts import SpotifyCharts
from datetime import datetime, timedelta
import csv
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
import os
import time
from datetime import datetime
import requests
import statistics

# Collect Daily Chart data for GB
api = SpotifyCharts.SpotifyCharts()

#today = date.today()
#print("Today's date:", today)
dateStr = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')
fileNameGB = 'top200_global_' + dateStr + '.csv'
print(fileNameGB)

api.top200Daily(output_file = fileNameGB, start = dateStr, end = dateStr, region = 'global')


ids = []
import csv

with open(fileNameGB, newline='') as csvfile:
    try:
        reader = csv.DictReader(csvfile)
        for row in reader:
            ids.append(row['spotify_id'])
    except UnicodeDecodeError:
        pass

while '' in ids:
    ids.remove('')

#print(ids)



os.environ["username"] = "Luke Hillery"
scope = "playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative user-read-recently-played user-top-read user-read-playback-position app-remote-control streaming user-library-modify user-library-read user-read-playback-state user-modify-playback-state user-read-currently-playing"
os.environ["SPOTIPY_CLIENT_ID"] = "3f203afa2be240ffbcaa571e12eee03e"
os.environ["SPOTIPY_CLIENT_SECRET"] = "6947e86380b949d1b5665125bf4dfd4c"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:8888/callback"

# =============================================================================
# getTrackMood - Takes a track id and returns its valence
# =============================================================================
def getTrackMood(id,sp):
  features = sp.audio_features(id)
  valence = features[0]['valence']
  energy = features[0]['energy']
  danceability = features[0]['danceability']
  tempo = features[0]['tempo']

  track_mood = [valence, energy, danceability, tempo]
  return track_mood

#==============================================================================
def getChartMood(ids, your_username, scope, client_id, client_secret, redirect_uri):

    token = util.prompt_for_user_token(
        username=your_username,
        scope=scope,
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri)

    # Create spotify object with permissions
    #spotifyObject = spotipy.Spotify(auth=token) #Leah's one
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    tracklist = []
    for i in ids:
        try:
            tracklist.append(getTrackMood(i,sp))
        except:
            pass
    return tracklist

def getAverageMood(tracklist):
    avg_tempo = statistics.mean(Extract4th(tracklist))
    avg_danceability = statistics.mean(Extract3rd(tracklist))
    avg_valence = statistics.mean(Extract1st(tracklist))
    avg_energy = statistics.mean(Extract2nd(tracklist))

    stdev_tempo = statistics.stdev(Extract4th(tracklist))
    stdev_danceability = statistics.stdev(Extract3rd(tracklist))
    stdev_valence = statistics.stdev(Extract2nd(tracklist))
    stdev_energy = statistics.stdev(Extract1st(tracklist))
    print('============================================')
    print('**GLOBAL CHART SUMMARY**')
    print('Global chart mean valence: {:.3f}, deviation = {:.3f}'.format((avg_valence),(stdev_valence)))
    print('Global chart mean energy: {:.3f}, deviation = {:.3f}'.format((avg_energy),(stdev_energy)))
    print('Global chart mean danceability: {:.3f}, deviation = {:.3f}'.format((avg_danceability),(stdev_danceability)))
    print('Global chart mean tempo: {:.3f}, deviation = {:.3f}'.format((avg_tempo),(stdev_tempo)))
    print('============================================')
# =============================================================================
# getPlaylistMood - Takes a playlist id and returns the avg mood of the tracks
# =============================================================================
def Extract1st(lst):
    return [item[0] for item in lst]
def Extract2nd(lst):
    return [item[1] for item in lst]
def Extract3rd(lst):
    return [item[2] for item in lst]
def Extract4th(lst):
    return [item[3] for item in lst]




chart_mood = getChartMood(ids,"Luke Hillery",scope,"3f203afa2be240ffbcaa571e12eee03e","6947e86380b949d1b5665125bf4dfd4c","http://localhost:8888/callback")
getAverageMood(chart_mood)
