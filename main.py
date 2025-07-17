import requests
from urllib.parse import urlencode
import base64
import webbrowser
from settings import client_id, secret, playlist

auth_headers = {
    "cliant_id": client_id,
    "response_type": "code",
    "redirect_url": "http://localhost:7777/callback",
    "scope": "user-library-read"
}

webbrowser.open("https://accounts.spotify.com/authorize?" + urlencode(auth_headers))

encoded_credentials = base64.b64encode(client_id.encode() + b':' + secret.encode()).decode("utf-8")

token_headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

token_data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": secret
}

r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)

token = r.json()["access_token"]

request_header = {
    "Authorization": 'Bearer ' + token,
    "Content-Type": "application/json"
}

if playlist.split("/")[0] == "https:":
    playlist_id = playlist.split("/")
else:
    playlist_id = [playlist]

url = f"https://api.spotify.com/v1/playlists/{playlist_id[-1]}"

playlist_get = requests.get(url, headers=request_header)

playlist_data = playlist_get.json()["tracks"]

songs = []

for i in playlist_data["items"]:
    current_song = i["track"]
    songs.append((f"{current_song["name"]} - {current_song["artists"][0]["name"]}", current_song["duration_ms"]))

time_in = 0
songs_lazy_new = []

for i in range(len(songs)):
    songs_lazy_new.append((songs[i][0], int(time_in / (1000 * 60 * 60) % 24), int((time_in / (1000 * 60)) % 60), int((time_in / 1000) % 60)))
    time_in += songs[i][1]

try:
    output = open("results.txt", "x")
    output.write("Playlist Results\n\n")
except Exception as e:
    output = open("results.txt", "a")
    output.write("\n\nNext results\n\n")

output = open("results.txt", "a")
for i in range(len(songs_lazy_new)):
    output.write(f"\n{songs_lazy_new[i][0]} is {songs_lazy_new[i][1]}H {songs_lazy_new[i][2]}M {songs_lazy_new[i][3]}S into your playlist")