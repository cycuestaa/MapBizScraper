import requests
import pandas as pd
import time

API_KEY = 'ur api'
ZIP_CODES = ['00907', '00909', '00911', '00912', '00913', '00901', '00918', '00915']
SEARCH_TERMS = ["nail salon", "hair salon", "tattoo", "barber", "pet grooming", "eyelashes"]

RADIUS = 1609  # 1 mile in meters
unique_places = {}

def get_coordinates(zip_code):
    geo_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={zip_code}&key={API_KEY}'
    res = requests.get(geo_url).json()
    location = res['results'][0]['geometry']['location']
    return location['lat'], location['lng']

def search_places(lat, lng, keyword):
    places_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': f'{lat},{lng}',
        'radius': RADIUS,
        'keyword': keyword,
        'key': API_KEY
    }
    res = requests.get(places_url, params=params).json()
    return res.get('results', [])

def get_place_details(place_id):
    details_url = 'https://maps.googleapis.com/maps/api/place/details/json'
    params = {
        'place_id': place_id,
        'fields': 'name,formatted_phone_number,website',
        'key': API_KEY
    }
    response = requests.get(details_url, params=params).json()
    return response.get('result', {})

data = []

for zip_code in ZIP_CODES:
    lat, lng = get_coordinates(zip_code)
    for term in SEARCH_TERMS:
        print(f"Searching: {term} in {zip_code}")
        businesses = search_places(lat, lng, term)
        for b in businesses:
            pid = b['place_id']
            if pid not in unique_places:
                details = get_place_details(pid)
                unique_places[pid] = {
                    'ZIP Code': zip_code,
                    'Name': b.get('name'),
                    'Address': b.get('vicinity'),
                    'Phone': details.get('formatted_phone_number'),
                    'Website': details.get('website'),
                    'Rating': b.get('rating'),
                    'Business Status': b.get('business_status'),
                    'Search Terms': [term],
                    'Google Maps URL': f"https://www.google.com/maps/place/?q=place_id:{pid}"
                }
            else:
                if term not in unique_places[pid]['Search Terms']:
                    unique_places[pid]['Search Terms'].append(term)
            time.sleep(0.3)

# Convert to list with comma-separated search terms
data = []
for info in unique_places.values():
    info['Search Terms'] = ", ".join(info['Search Terms'])
    data.append(info)

df = pd.DataFrame(data)
df.to_excel("beauty_businesses_filtered-PR1.xlsx", index=False)
print("✅ Done! File saved as beauty_businesses_filtered-PR1.xlsx")
