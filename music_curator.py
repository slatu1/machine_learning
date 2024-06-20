import spotipy
import spotipy.util as util

import os
import csv
import math
import user
from song import *
import time
# Keys to get from System Variables that allow access to Spotify API
# client_id = os.environ.get('SPOTIFY_CLIENT_ID_KEY')
# client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET_KEY')
# redirect = os.environ.get('SPOTIFY_REDIRECT_URL')

# Scope for personal token usage
scope = 'user-library-read'

# Interacts with Spotify API and gets data for all the songs in 4
# playlists where each playlist represents Rap, Pop, Rock, and Country
# Writes all the data to a CSV

def exportData(spotify_personal,filename,data):

    # CSV File writer
    csv_file = open(filename, 'w', newline='', encoding='utf-8')
    spam_writer = csv.writer(csv_file, delimiter=',')

    # Columns in CSV File
    spam_writer.writerow(["Song_Name", "Artist", "Danceability", "Energy", "Key", "Loudness", 				"Speechiness","Acousticness", "Instrumentalness", "Liveness", "Valence", 				"Temp", "Like"])
    
    #song_features = spotify_personal.audio_features([x.GetId() for x in data])
    # Loops through the audio features for all the songs and writes them to CSV File
    for i,s in enumerate(data):
        #print(spotify_personal.track(s.GetId())['name'])
        ssong = spotify_personal.track(s.GetId())
        print(ssong['id'])
        print(ssong['name'])
        print(song_features[i])
        #print(spotify_personal.audio_features(ssong['id']))
        #ssong = spotify_personal.track(s.GetId())
        song_features = spotify_personal.audio_features(s.GetId())
        spam_writer.writerow([ssong['name'],
                     ssong['album']['artists'][0]['name'],
                     song_features[0]["danceability"],
                     song_features[0]["energy"],
                     song_features[0]["key"],
                     song_features[0]["loudness"],
                     song_features[0]["speechiness"],
                     song_features[0]["acousticness"],
                     song_features[0]["instrumentalness"],
                     song_features[0]["liveness"],
                     song_features[0]["valence"],
                     song_features[0]["tempo"],
                     str(s.GetLike())])
        time.sleep(0.05)                     
    
    # Closes CSV File so it can be used immediately
    csv_file.close()
            
def get_test_data(spotify_personal):
    test_data = []
    # testing data -- thumbs down
    playlist = spotify_personal.playlist_tracks('https://open.spotify.com/playlist/3nCJjwznOmIpvbJj8aa9XI')
    print(playlist)
    print(str(len(playlist))+'\n')
    for i in playlist['items']:
        test_data.append(song(i['track']['id'],0))
        print(str(i['track']['name']) + '\n')
    
    # testing data -- thumbs up
    playlists = ['https://open.spotify.com/playlist/4errb5oEhiC5jfW7wKkJea',
    		'https://open.spotify.com/playlist/2d6BPNUwM78SOmdlrqv9fI',
    		'https://open.spotify.com/playlist/0NkiulhjGpVY1rgqEHwFcy',
    		'https://open.spotify.com/playlist/6rBxMlCxZzZTsH2W85MSUx']
    for i in playlists:
        for t in spotify_personal.playlist_tracks(i)['items']:
            #print(t)
            test_data.append(song(t['track']['id'],1))
            print(t['track']['name'])
            
    print('\n\n from ref \n\n')
    for s in test_data:
        print(str(spotify_personal.track(s.GetId())['name']) + '\t' + str(s.GetLike())) 
        
    return test_data        
        
def print_songs(spotify_personal, username, num_songs):

    print("Interacting with Spotify API\n")
    new_data = []
    # Spotify Playlist URLs
    list_playlists = ["spotify:playlist:59ixZkMDuc2Qpq9DGzue7r",  # Rap
                      "spotify:playlist:4noDy1IQejcxDbTLvzuWhS",  # Pop
                      "spotify:playlist:37i9dQZF1DX3rxVfibe1L0",  # Country
                      "spotify:playlist:7IDCJaW0CvutAyMbSvheGK"]  # Metal

    list_rating = [1,   # Rap
                   0,   # Pop
                   -1,  # Country
                   -2]  # Metal

    songs_url = []
    albums = []
    

    # Extracts all the song URLs from the response to run through another API endpoint
    for i in spotify_personal.new_releases(limit=1)['albums']['items']:
        #print(i['artists'][0]['name'])
        #print(i['name']) #name of the track
        #print(i['external_urls']) #artist of the t
        #print('\n') 
        print(spotify_personal.album_tracks(i['id'])) #artist of the t
        #new_data.append(song(i['id'],None))
        print('\n\n') 
        albums.append(i['id'])
        time.sleep(0.05)
        

    for k in albums:
        #print(k)
        for m in spotify_personal.album_tracks(k)['items']:
            print(m['name'])
            #print(m['artists'][0]['track']['name'])
            new_data.append(song(m['id'],None))
            #print(m['name'])
            #songs_url.append(m['uri'])
        #print('\n')

        # songs_url.append(playlists['items'][k]['track']['external_urls']['spotify'])

    for s in new_data:
        print(str(spotify_personal.track(s.GetId())['name']) + '\t' + str(s.GetLike())) 
        
    print("Done downloading data \n")
    return new_data
    
def main():

    # user = ""

    spotify_personal = None

    if spotify_personal is None:
        personal_token = util.prompt_for_user_token(user.username,
                                                    scope,
                                                    user.client_id,
                                                    user.client_secret,
                                                    user.redirect)

        # API Wrapper objects to use functions to interact with Spotify API
        #spotify_personal = spotipy.Spotify(auth=personal_token,requests_timeout=1)
        spotify_personal = spotipy.Spotify(auth=personal_token)
        # Username of person logged in
        username = spotify_personal.current_user()["id"] 
    #for i in spotify_personal.new_releases(limit=20)['albums']['items']:
        #print(i['artists'][0]['name'])
        #print(i['name']) #name of the track
        #print(i['external_urls']) #artist of the t
        #print('\n') 
        
    print('\n')  
    #print(spotify_personal.new_releases(limit = 1))
    #print(spotify_personal.new_releases(limit = 1)["id"])
    #testData = get_test_data(spotify_personal)
    #exportData(spotify_personal,"test_data.csv",testData)
    newData = print_songs(spotify_personal, username, 1) 
    exportData(spotify_personal,"new_data.csv",newData)   
    
# Program entrance
if __name__ == "__main__":
    main()