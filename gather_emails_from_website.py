import pandas as pd
import re
import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin

EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
CONTACT_KEYWORDS = ['contact', 'contacto', 'contactar', 'contáctanos', 'contactanos']
MEDIA_KEYWORDS = ['media', 'prensa', 'press', 'medios']
SOCIAL_PLATFORMS = {
    'Instagram': 'instagram.com',
    'Facebook': 'facebook.com',
    'Pinterest': 'pinterest.com',
    'TikTok': 'tiktok.com',
    'Twitter': 'twitter.com',
    'X': 'x.com'
}
def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        print(text.encode('ascii', 'ignore').decode())


def extract_emails_from_text(text, keywords=[]):
    emails = re.findall(EMAIL_REGEX, text)
    if keywords:
        filtered_emails = [e for e in emails if any(k in text.lower() for k in keywords)]
        return filtered_emails or emails
    return emails

def extract_emails_from_url(url):
#    headers = {'User-Agent': 'Mozilla/5.0'}
#    response = requests.get(url, headers=headers, timeout=5)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }


    result = {
    'main_page_email': None,
    'contact_page_email': None,
    'media_inquiry_email': None,
    'Instagram': None,
    'Facebook': None,
    'Pinterest': None,
    'TikTok': None,
    'Twitter': None
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        print(f"first print")

    except requests.exceptions.RequestException as e:
        print(f" Connection failed for main page: {url} ") #— {e}")
        return result  # Skip to the next row

    try:
        print(f" VISITING: {url}")
        #response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')


        # 1. Try mailto: link from main page
        mailto_links = soup.select('a[href^=mailto]')
        if mailto_links:
            email_from_mailto = mailto_links[0].get('href').replace('mailto:', '').strip()
            result['main_page_email'] = email_from_mailto


        # 2. Try regex on visible text
        text = soup.get_text()
        emails = extract_emails_from_text(text)
        
        #2.. 
        media_emails = extract_emails_from_text(text, MEDIA_KEYWORDS)

        if media_emails:
            result['media_inquiry_email'] = media_emails[0]

         # If no main page email yet, try regex
        if not result['main_page_email']:
            all_emails = extract_emails_from_text(text)
            if all_emails:
                result['main_page_email'] = all_emails[0]

        # 3. Extract social media links
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href'].lower()
            for platform, domain in SOCIAL_PLATFORMS.items():
                if domain in href and not result.get(platform):
                    result[platform] = href

        # 4. Look for a contact page and repeat search there
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href'].lower()
            anchor_text = a_tag.get_text(strip=True).lower()
            if any(k in href for k in CONTACT_KEYWORDS) or any(k in anchor_text for k in CONTACT_KEYWORDS):
                contact_url = urljoin(url, href)
                print(f" Found contact page: {contact_url}")
                try:
                    #contact_resp = requests.get(contact_url, headers=headers, timeout=5)
                    try:
                        contact_resp = requests.get(contact_url, headers=headers, timeout=5)
                    except requests.exceptions.RequestException as e:
                        print(f" Failed to connect to contact page: {contact_url} ")# {e}")
                        continue  # Skip this contact page attempt

                    contact_soup = BeautifulSoup(contact_resp.text, 'html.parser')

                    # Try mailto on contact page
                    contact_mailto = contact_soup.select('a[href^=mailto]')
                    if contact_mailto:
                        result['contact_page_email'] = contact_mailto[0].get('href').replace('mailto:', '').strip()
                    else:
                        contact_text = contact_soup.get_text()
                        contact_emails = extract_emails_from_text(contact_text)
                        if contact_emails:
                            result['contact_page_email'] = contact_emails[0]

                except Exception as e:
                    print(f" Failed to load contact page: {contact_url} ")# {e}")
                break  # only check one contact link

    except Exception as e:
        print(f" Error with URL: {url} ")# {e}")
    
    return result

# Load spreadsheet
df = pd.read_excel("beauty_businesses_filtered-PR2.xlsx")

# For test: limit to 50 rows
df = df.head(10)

# Create email column with progress tracking
emails = []
for index, row in df.iterrows():
    url = row['Website']
    print(f" [{index+1}/{len(df)}] Checking: {url} | ")
    #email = extract_email_from_url(url) if pd.notnull(url) else None
    #emails.append(email)
    result =  extract_emails_from_url(url) if pd.notnull(url) else {}
    for key, value in result.items():
        df.at[index, key] = value
    time.sleep(1) # delay getting blocked

#df['Email'] = emails
df.to_excel("PR_biz_contacts.xlsx", index=False)
print(" Email scraping complete! File saved as 'PR_biz_contacts.xlsx'")
