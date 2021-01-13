from fycharts import SpotifyCharts
from datetime import datetime, timedelta
import csv
import config
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
fileNameGB = 'top200_gb_' + dateStr + '.csv'
print(fileNameGB)

api.top200Daily(output_file = fileNameGB, start = dateStr, end = dateStr, region = 'gb')


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
print(ids)

os.environ["username"] = config.username
scope = "playlist-modify-public playlist-modify-private playlist-read-private playlist-read-collaborative user-read-recently-played user-top-read user-read-playback-position app-remote-control streaming user-library-modify user-library-read user-read-playback-state user-modify-playback-state user-read-currently-playing"
os.environ["SPOTIPY_CLIENT_ID"] = config.SPOTIPY_CLIENT_ID
os.environ["SPOTIPY_CLIENT_SECRET"] = config.SPOTIPY_CLIENT_SECRET
os.environ["SPOTIPY_REDIRECT_URI"] = config.SPOTIPY_REDIRECT_URI

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
    print('**GB CHART SUMMARY**')
    print('GB Chart mean valence: {:.3f}, deviation = {:.3f}'.format((avg_valence),(stdev_valence)))
    print('GB Chart mean energy: {:.3f}, deviation = {:.3f}'.format((avg_energy),(stdev_energy)))
    print('GB Chart mean danceability: {:.3f}, deviation = {:.3f}'.format((avg_danceability),(stdev_danceability)))
    print('GB Chart mean tempo: {:.3f}, deviation = {:.3f}'.format((avg_tempo),(stdev_tempo)))
    SessionRequestToThingspeak = 'https://api.thingspeak.com/update?api_key=L4P6XPRO3ODASMS3&field5='+str(avg_valence)+'&field6='+str(avg_energy)+'&field7='+str(avg_danceability)+'&field8='+str(avg_tempo)
    request = requests.get(SessionRequestToThingspeak)
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




chart_mood = getChartMood(ids,config.username,scope,config.SPOTIPY_CLIENT_ID,config.SPOTIPY_CLIENT_SECRET,config.SPOTIPY_REDIRECT_URI)
getAverageMood(chart_mood)
