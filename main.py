from bs4 import BeautifulSoup
from datetime import date
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# secrets
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_SECRET"
URI = "http://bilboardspotipy.com/callback/"

# billboard scrapping
target_date = input("Which year do you want to travel to? Type the date in this format: YYYY-MM-DD")
print(date.fromisoformat(target_date))

url = "https://www.billboard.com/charts/hot-100/" + str(date.fromisoformat(target_date)) + "/"
print(url)

response = requests.get(url)
web_page = response.text

soup = BeautifulSoup(web_page, 'html.parser')
songs_html_list = soup.select(selector='li #title-of-a-story')
songs_list = []

for song in songs_html_list:
    text = song.getText().strip()
    songs_list.append(text)

print(songs_list)

# spotipy SpotifyOAuth authorization
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

# asking spotify for uris
item_list = []
for index in range(100):
    song = songs_list[index]
    query = sp.search(q=f"track:{song}", type="track", limit=1, market="US")
    try:
        song_uri = query["tracks"]["items"][0]["uri"]
    except IndexError:
        print(f"track {song} not found")
        continue
    else:
        item_list.append(song_uri)

print(item_list)
user_id = sp.current_user()["id"]
print(user_id)

# creating a spotify playlist
playlist = sp.user_playlist_create(user=user_id, name=f"{target_date} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=item_list)

