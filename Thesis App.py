import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import http.client

connection = http.client.HTTPSConnection("track-analysis.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "722e6527famshdb623ffad869568p1cef05jsn0db7275ad6d2",
    'x-rapidapi-host': "track-analysis.p.rapidapi.com"
}
spotify_data = pd.read_csv("C:/Users/jacob/OneDrive/Desktop/Code/Projects/Thesis App/Thesis App/data/spotify song data/tracks.csv")
screen_width = 400
screen_height = 600
bg_color = 'darkblue'
widget_bg_color='lightblue'
spotify_clientID = "4fc9da5879ee48df8a948d805e79e203"
spotify_secret = "f02c0751e61149398500e5f208ec788e"
redirect_uri = "https://duckduckgo.com" ## This URL doesn't matter as long as it is valid. 
GENRE_SEEDS = [
    "acoustic", "afrobeat", "alt-rock", "alternative", "ambient", "anime",
    "black-metal", "bluegrass", "blues", "bossanova", "brazil", "breakbeat",
    "british", "cantopop", "chicago-house", "children", "chill", "classical",
    "club", "comedy", "country", "dance", "dancehall", "death-metal", "deep-house",
    "detroit-techno", "disco", "disney", "drum-and-bass", "dub", "dubstep",
    "edm", "electro", "electronic", "emo", "folk", "forro", "french", "funk",
    "garage", "german", "gospel", "goth", "grindcore", "groove", "grunge",
    "guitar", "happy", "hard-rock", "hardcore", "hardstyle", "heavy-metal",
    "hip-hop", "holidays", "honky-tonk", "house", "idm", "indian", "indie",
    "indie-pop", "industrial", "iranian", "j-dance", "j-idol", "j-pop", "j-rock",
    "jazz", "k-pop", "kids", "latin", "latino", "malay", "mandopop", "metal",
    "metal-misc", "metalcore", "minimal-techno", "movies", "mpb", "new-age",
    "new-release", "opera", "pagode", "party", "philippines-opm", "piano", "pop",
    "pop-film", "post-dubstep", "power-pop", "progressive-house", "psych-rock",
    "punk", "punk-rock", "r-n-b", "rainy-day", "reggae", "reggaeton", "road-trip",
    "rock", "rock-n-roll", "rockabilly", "romance", "sad", "salsa", "samba",
    "sertanejo", "show-tunes", "singer-songwriter", "ska", "sleep", "songwriter",
    "soul", "soundtracks", "spanish", "study", "summer", "swedish", "synth-pop",
    "tango", "techno", "trance", "trip-hop", "turkish", "work-out", "world-music"
]
SEARCH_SEEDS = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
]

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_clientID,client_secret=spotify_secret,redirect_uri=redirect_uri,scope='user-modify-playback-state,user-read-playback-state'))

## Spotify's Web API doesn't allow you to pick a truly "random" song.
## To combat this, we will choose a random genre as a "seed".
## This seed will then be used to search for songs in that genre, where one will be picked at random.

def get_audio_features(track_id): ## Uses TrackNet RapidAPI, spotify sucks now :(
    connection.request("GET", f"/pktx/spotify/{track_id}", headers=headers)
    features = connection.getresponse().read()
    return features.decode("utf-8")

def random_song():
    genre = np.random.choice(GENRE_SEEDS)
    char = np.random.choice(SEARCH_SEEDS)
    offset = np.random.randint(0,1000) ## Spotify only returns 1000 songs for any given search, and we want to pick a random one from that 1000.
    results = spotify.search(q=f"genre:'{genre}' {char}", type="track", limit=1, offset=offset)
    items = results['tracks']['items']

    try: ## Sometimes if offset is too large, the list items[] doesn't have enough indices.
        track = items[0]
        audio_features = get_audio_features(track['id'])
        if not len(audio_features):
            raise Exception
        print(audio_features)
        spotify.start_playback(uris=[track['uri']])
        return track['name']
    except:
        return random_song()

def handle_song_button_press():
    song_button_text.set(random_song())

def handle_rating_button_press(x):
    print(x)
    handle_song_button_press()

def handle_generic_GUI(gui):
    playing_label = ttk.Label(gui,text="Now Playing...",font=("Helvetica", 16),background=widget_bg_color)
    playing_label.place(x=screen_width/2,y=screen_height/5,anchor='center')

    title_label = ttk.Label(gui,text="Thesis Data Collection", font=("Helvetica", 24), background=widget_bg_color)
    title_label.place(x=screen_width/2,y=screen_height/10,anchor='center',width=320,height=50)

    question1_label = ttk.Label(gui,text="How much do you like this song?", font=("Helvetica", 12), background=widget_bg_color)
    question1_label.place(x=screen_width/2,y=screen_height/3,anchor='center',width=230,height=25)

    for i in range(1,11):
        middle_offset=12.5
        button=ttk.Button(gui,text=str(i),command=lambda x=i: handle_rating_button_press(x))
        x_loc = ((i-5)*25) + screen_width/2 - middle_offset
        button.place(x=x_loc,y=screen_height/2.5, anchor='center', width=22)

## Window Configuration
gui = tk.Tk()
gui.title("Thesis App")
gui.geometry(f"{screen_width}x{screen_height}")
gui.configure(bg=bg_color)

song_button_text = tk.StringVar()
song_button_text.set(random_song())
song_button = ttk.Button(gui,textvariable=song_button_text,command=handle_song_button_press)
song_button.place(x=screen_width/2, y=screen_height/4, anchor='center')

handle_generic_GUI(gui)
gui.mainloop()