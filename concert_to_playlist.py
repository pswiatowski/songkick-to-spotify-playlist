import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import json
import calendar
from datetime import datetime

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
SCOPE = "playlist-modify-private"

def load_concerts(json_file):
    with open(json_file, "r", encoding="utf-8") as f:
        concerts = json.load(f)
    return concerts

def group_concerts_by_month(concerts):
    grouped = {}
    for concert in concerts:

        date_str = concert.get("start_time", "")
        if not date_str:
            continue
        
        date_obj = datetime.fromisoformat(date_str)
        month_year = f"{date_obj.year}-{date_obj.month:02d}"
        
        if month_year not in grouped:
            grouped[month_year] = []
        grouped[month_year].append(concert)
    return grouped

def get_artist_uri(sp, artist_name):
    results = sp.search(q=f"artist:{artist_name}", type="artist", limit=1)
    if results["artists"]["items"]:
        return results["artists"]["items"][0]["id"]
    return None

def get_top_tracks(sp, artist_uri):
    results = sp.artist_top_tracks(artist_uri)
    return [track["uri"] for track in results["tracks"]]

def create_playlist(sp, month_year, tracks):
    playlist_name = f"Zurich Concerts {month_year}"
    
    playlist = sp.user_playlist_create(sp.current_user()["id"], playlist_name, public=False)
    print(f"Created playlist: {playlist_name}")

    chunk_size = 100
    for i in range(0, len(tracks), chunk_size):
        chunk = tracks[i:i + chunk_size]
        sp.playlist_add_items(playlist["id"], chunk)
        print(f"Added {len(chunk)} tracks to {playlist_name}")

def main():
    print("Loading concerts_by_month")
    concerts = load_concerts("zurich_concerts.json")
    
    print("Grouping concerts by month")
    concerts_by_month = group_concerts_by_month(concerts)
    
    print("Spotify auth")
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SCOPE
    ))
    
    for month_year, concerts in concerts_by_month.items():
        print(f"Processing {month_year}...")
        all_tracks = []
        
        for concert in concerts:
            artists = concert.get("artists", "").split(", ")
            for artist in artists:
                artist_uri = get_artist_uri(sp, artist)
                if artist_uri:
                    print(f"arist {artist} found")
                    tracks = get_top_tracks(sp, artist_uri)
                    all_tracks.extend(tracks[:5]) 
                else:
                    print(f"arist {artist} not found")
        
        if all_tracks:
            create_playlist(sp, month_year, all_tracks)
        else:
            print(f"No tracks found for {month_year}")

if __name__ == "__main__":
    main()

