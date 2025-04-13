import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

EMAIL_REGEX = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

def extract_email_from_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 1. Try mailto: link
        mailto_links = soup.select('a[href^=mailto]')
        if mailto_links:
            return mailto_links[0].get('href').replace('mailto:', '')

        # 2. Try regex on page text
        text = soup.get_text()
        emails = re.findall(EMAIL_REGEX, text)
        if emails:
            return emails[0]

        # 3. Look for a contact page link and repeat search
        contact_link = None
        for a_tag in soup.find_all('a', href=True):
            if 'contact' in a_tag['href'].lower():
                contact_link = urljoin(url, a_tag['href'])
                break

        if contact_link:
            response = requests.get(contact_link, headers=headers, timeout=5)
            soup = BeautifulSoup(response.text, 'html.parser')
            mailto_links = soup.select('a[href^=mailto]')
            if mailto_links:
                return mailto_links[0].get('href').replace('mailto:', '')
            text = soup.get_text()
            emails = re.findall(EMAIL_REGEX, text)
            if emails:
                return emails[0]
        return None
    except Exception as e:
        print(f"❌ Error with URL: {url} — {e}")
        return None

# Load spreadsheet
df = pd.read_excel("beauty_businesses_filtered-PR1.xlsx")

# For test: limit to 50 rows
# df = df.head(50)

# Create email column with progress tracking
emails = []
for index, row in df.iterrows():
    url = row['Website']
    print(f"🔍 [{index+1}/{len(df)}] Checking: {url}")
    email = extract_email_from_url(url) if pd.notnull(url) else None
    emails.append(email)

df['Email'] = emails
df.to_excel("beauty_businesses_with_emails-PR1.xlsx", index=False)
print("✅ Email scraping complete! File saved as 'beauty_businesses_with_emails-PR1.xlsx'")
