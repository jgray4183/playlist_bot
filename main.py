import requests
from urllib.parse import urlencode
import webbrowser
from settings import client_id, secret, playlist

#API auth code

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

#this section tests if you have given a full playlist link or just the Spotify ID and can handle either
if playlist.split("/")[0] == "https:":
    playlist_id = playlist.split("/")
else:
    playlist_id = [playlist]

url = f"https://api.spotify.com/v1/playlists/{playlist_id[-1]}"

#gets playlist from the API, this only pulls the first 100 songs as I can't work out how to get offset to work for this
playlist_get = requests.get(url, headers=request_header)

playlist_data = playlist_get.json()["tracks"]

#itirates over the tracks in the playlist to get the name and artist of the song, at the same time converts the milliseconds into the playlist to HMS then increases that veriable in place for the current song
songs = []
ms_into_playlist = 0

for i in playlist_data["items"]:
    current_song = i["track"]
    songs.append({"Song Name & Artist": f"{current_song["name"]} - {current_song["artists"][0]["name"]}", "Hours in": int(ms_into_playlist / (1000 * 60 * 60) % 24), "Minutes in": int((ms_into_playlist / (1000 * 60)) % 60), "Seconds in": int((ms_into_playlist / 1000) % 60)})
    ms_into_playlist += current_song["duration_ms"]

#writes the list to a txt file
try:
    output = open("results.txt", "x")
    output.write("Playlist Results\n\n")
except Exception as e:
    output = open("results.txt", "a")
    output.write("\n\n\nNext results\n\n")

output = open("results.txt", "a")
for i in range(len(songs)):
    output.write(f"\n{songs[i]["Song Name & Artist"]} is {songs[i]["Hours in"]}H {songs[i]["Minutes in"]}M {songs[i]["Seconds in"]}S into your playlist")