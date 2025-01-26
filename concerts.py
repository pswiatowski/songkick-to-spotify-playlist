import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.songkick.com/metro-areas/104761-switzerland-zurich?page={}"

def extract_concerts_from_page(page_number):
    url = BASE_URL.format(page_number)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    container = soup.find("ul", class_="component metro-area-calendar-listings dynamic-ad-container")
    if not container:
        print(f"No events found on page {page_number}")
        return []
    
    concerts = []
    event_list = container.find_all("li", class_="event-listings-element")
    
    for event_li in event_list:
        # Extract the date
        date = event_li.get("title", "").strip()
        
        artist_tag = event_li.select_one(".artists strong")
        artists = artist_tag.text.strip() if artist_tag else "Unknown Artists"
        
        venue_tag = event_li.select_one(".venue-link")
        venue = venue_tag.text.strip() if venue_tag else "Unknown Venue"
        
        city_tag = event_li.select_one(".city-name")
        city = city_tag.text.strip() if city_tag else "Unknown City"

        microformat_script = event_li.select_one(".microformat script")
        if microformat_script:
            microformat_json = json.loads(microformat_script.string)
            event_details = microformat_json[0]
            start_time = event_details.get("startDate", "Unknown Start Date")
            event_url = event_details.get("url", "No URL Available")
        else:
            start_time = "Unknown Start Date"
            event_url = "No URL Available"
        
        concerts.append({
            "date": date,
            "artists": artists,
            "venue": venue,
            "city": city,
            "start_time": start_time,
            "event_url": event_url
        })
    
    return concerts

def scrape_all_pages(total_pages):
    all_concerts = []
    for page_number in range(1, total_pages + 1):
        print(f"Scraping page {page_number}...")
        concerts = extract_concerts_from_page(page_number)
        all_concerts.extend(concerts)
        time.sleep(2)  # Pause to avoid overwhelming the server
    return all_concerts

total_pages = 13
all_concerts = scrape_all_pages(total_pages)

output_file = "zurich_concerts.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_concerts, f, ensure_ascii=False, indent=4)

print(f"Scraped {len(all_concerts)} concerts and saved to {output_file}")
