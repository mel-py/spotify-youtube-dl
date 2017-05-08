import spotipy
import spotipy.util as util
import youtube_dl
import urllib
import urllib2
from bs4 import BeautifulSoup

def get_songs():
    playlist = raw_input("Enter playlist URL: ")
    
    #strip the username and playlist id
    split_url = playlist.split('/')
    username = split_url[-3]
    playlist_id = split_url[-1]

    #get access token
    token = util.prompt_for_user_token(username, 'playlist-modify-public')
        
    if token:
        found_tracks = []
        
        sp = spotipy.Spotify(auth=token)
        results = sp.user_playlist(username, playlist_id, fields='tracks,next')
        tracks = results['tracks']
        for item in tracks['items']:
            track = item['track']
            found_tracks.append(track['name'] + ' - ' + track['artists'][0]['name'])
        return found_tracks
    else:
        print("Can't get token for " +  username)
        exit

def download_songs(songs):
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    ydl = youtube_dl.YoutubeDL(options)
    
    for song in songs:
        print('Downloading ' + song + '...')

        #find the song
        query = urllib.quote(song)
        url = "https://www.youtube.com/results?search_query=" + query
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html)
        #get the url of the found video
        vid = 'https://www.youtube.com' + soup.find(attrs={'class':'yt-uix-tile-link'})['href']
        print(vid)
        
        #download the audio
        with ydl:
            ydl.download([vid])
            
songs = get_songs()
download_songs(songs)
