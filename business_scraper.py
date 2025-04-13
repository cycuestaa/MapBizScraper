import requests
import pandas as pd
import time
import argparse
import sys

API_KEY = 'AIzaSyAr7mTtobj2TIBgX507YavWpuaU86ZcWjw'
#ZIP_CODES = ['00907', '00909', '00911', '00912', '00913', '00901', '00918', '00915']
SEARCH_TERMS = ["nails", "nail salon", "makeup artist","hair salon", "beauty salon", "tattoo", "barber", "pet grooming", "eyelashes"]
RADIUS = 2400  # 1 mile in meters (1609)
unique_places = {}

def get_coordinates(zip_code):
    geo_url = f'https://maps.googleapis.com/maps/api/geocode/json?components=postal_code:{zip_code}|country:PR&key={API_KEY}'

    #address={zip_code}&key={API_KEY}'
    res = requests.get(geo_url).json()
    results = res.get('results', [])
    if not results:
        print(f" No location found for ZIP code: {zip_code}")
        return None, None

    location = results[0]['geometry']['location']
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

def main():
    parser = argparse.ArgumentParser(description='Scrape businesses by zip code.')
    parser.add_argument('csv_file', help='Path to CSV file with zipCode and neighborhoodName columns')
    args = parser.parse_args()

    try:
        df_zips = pd.read_csv(args.csv_file)
        zip_entries = df_zips[['zipCode', 'neighborhoodName']].dropna()
    except Exception as e:
        print(f"xx Error reading CSV file: {e}")
        sys.exit(1)

    for _, row in zip_entries.iterrows():
        zip_code = str(row['zipCode']).zfill(5)
        print(f" Using ZIP code: {zip_code}")
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
                        'Neighborhood': row['neighborhoodName'],
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

    # Save results
    data = []
    for info in unique_places.values():
        info['Search Terms'] = ", ".join(info['Search Terms'])
        data.append(info)

    df_out = pd.DataFrame(data)
    df_out.to_excel("beauty_businesses_filtered-PR2.xlsx", index=False)
    #df_out.to_csv("beauty_businesses_filtered-PR2.csv", index=False)
    print("Done! File saved as beauty_businesses_filtered-PR2.xlsx")

if __name__ == "__main__":
    main()
