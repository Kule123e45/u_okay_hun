![image](https://images.squarespace-cdn.com/content/v1/5a5e8b9c29f18756949ff438/1609954473115-W2LECPKPHRMNXHGQVM2H/ke17ZwdGBToddI8pDm48kClzf79BoNW-ZxHXoon2AjIUqsxRUqqbr1mOJYKfIPR7LoDQ9mXPOjoJoqy81S2I8N_N4V1vUb5AoIIIbLZhVYwL8IeDg6_3B-BRuF4nNrNcQkVuAT7tdErd0wQFEGFSnJu68DSmt4cMLdp4eAfYkcvb7DDBIcnQOKaITO_G9BHxDWoadAkUKudpHVI3VS5UPw/banner.jpg?format=1500w)
'U okay hun' is a web application designed to recognise sudden changes in Spotify listening patterns in order to detect deteriorating mental health. 
Sensing & IOT Module, Design Engineering, Imperial College London

[Read the report](https://www.lukehillery.com/u-okay-hun)

## 1. Data Collection
The Data_Collection/ directory contains all scripts and data backups used during part 1 of the coursework. These were loaded onto a Rasberry Pi.

File descriptions
spotify_live_data_with_sessions.py Data collection scripts for collecting live and session data from Spotify 
get_gb_charts.py and get_global_charts.py collect the list of top 200 songs in Great Britain and globally respectively. They use Spotify's API to collect track features and summarise the chart data.
Main.py Raw data collection script

## 2. Data Analysis
The Time_Series/ directory the Python data analytics.

[View the Jupyter Notebook](https://www.lukehillery.com/u-okay-hun)

Note: API keys and credential files have not been committed.

## 3. Application
The Application/ directory contains all files related to the web application created to alert the Spotify user and an emergency contact when their listening pattern deviates significantly from their usual mood. This application was created using flask.

## References:
- Information for implementing Spotify API
https://developer.spotify.com/documentation/web-api/
- Information for implementing FyCharts
https://pypi.org/project/fycharts/
- Information for implementing ThingSpeak API
https://thingspeak.com/
