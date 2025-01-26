
# songkick-to-spotify-playlist
Automatically create Spotify playlists featuring top tracks from artists performing at upcoming concerts in a specified area.

## Overview
This project fetches concert data from Songkick for a specific area (currently set to Zurich) and generates Spotify playlists featuring the top tracks from performing artists. Playlists are grouped by month, making it easy to discover and enjoy music from artists performing live in your area.

## Features
- Scrape concert data from Songkick for Zurich.
- Group concerts by month for easy organization.
- Fetch top tracks of performing artists using the Spotify API.
- Automatically create private Spotify playlists for each month.

## Installation and Usage

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/songkick-to-spotify-playlist.git
cd songkick-to-spotify-playlist
```

### 2. Set up a Python virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scriptsctivate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the project root with the following details:
```env
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
```
Replace `your_spotify_client_id` and `your_spotify_client_secret` with your Spotify developer credentials. You can obtain these by creating an app on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).

### 5. Run the Songkick scraper
Run the first script to scrape concert data from Songkick and save it to a JSON file:
```bash
python scrape_songkick.py
```
This will create a file named `zurich_concerts.json` containing all the concert details.

### 6. Generate Spotify playlists
Run the second script to create playlists for each month based on the scraped data:
```bash
python create_playlists.py
```

### 7. Enjoy your playlists!
Log in to your Spotify account and find the newly created playlists in your library.

## Scripts Overview

### `scrape_songkick.py`
- Scrapes concert data for Zurich from Songkick.
- Saves the data in `zurich_concerts.json`.

### `create_playlists.py`
- Reads concert data from `zurich_concerts.json`.
- Fetches top tracks for each artist using Spotify's API.
- Creates monthly playlists on Spotify.

## Example Output
After running the scripts, you will find playlists like:
- **Zurich Concerts 2025-01**: Featuring top tracks from artists performing in January 2025.
- **Zurich Concerts 2025-02**: Featuring top tracks from artists performing in February 2025.

## Limitations
- **Spotify API Limits**: A maximum of 100 tracks can be added per playlist request.
- **Songkick Location**: Currently hardcoded to Zurich. You can update the metro area ID for other locations.
- **Missing Artists**: Some artists may not have data on Spotify, resulting in fewer tracks in playlists.

## Future Improvements
- Add support for other cities by dynamically fetching metro area IDs.
- Optimize track selection with genre-based filters.
- Allow customization of playlist names and visibility (public or private).
