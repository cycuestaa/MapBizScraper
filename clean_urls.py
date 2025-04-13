import pandas as pd
from urllib.parse import urlparse
import os

# -------- CONFIG -------- #
# Input file name (must be in the same directory)
INPUT_FILE = "beauty_businesses_filtered-PR2.xlsx" #"PR_biz_contacts.xlsx"
OUTPUT_FILE = "cleaned_PR_biz_contacts.xlsx"

# Keyword groups for matching
SOCIAL_MEDIA_KEYWORDS = ['instagram', 'facebook', 'pinterest', 'twitter']
BOOKING_SITE_KEYWORDS = ['vagaro', 'booksy', 'fresha', 'glossgenius']

# -------- FUNCTIONS -------- #

def classify_website(url):
    """
    Classify a website URL into group and host.
    Group is one of: social media, booking site, website, or blank.
    Host is the matching keyword or domain core.
    """
    if pd.isna(url) or not isinstance(url, str) or not url.strip():
        return pd.Series(['', ''])

    # Normalize and parse the URL
    parsed = urlparse(url.strip())
    domain = parsed.netloc.lower() if parsed.netloc else parsed.path.lower()

    # Match against known keyword groups
    for keyword in SOCIAL_MEDIA_KEYWORDS:
        if keyword in domain:
            return pd.Series(['social media', keyword])
    for keyword in BOOKING_SITE_KEYWORDS:
        if keyword in domain:
            return pd.Series(['booking site', keyword])

    # Otherwise return as general website with extracted host
    if domain:
        root_parts = domain.split('.')
        host = root_parts[-2] if len(root_parts) >= 2 else domain
        return pd.Series(['website', host])

    return pd.Series(['', ''])

# -------- MAIN PROGRAM -------- #

# Locate and load the dataset

try:
    df = pd.read_excel(INPUT_FILE)
    print(f"Loaded file: {INPUT_FILE}")
except FileNotFoundError:
    raise FileNotFoundError(f"Could not find file: {INPUT_FILE}")

# Verify required column
if 'Website' not in df.columns:
    raise ValueError("The input file must contain a column named 'Website'.")

# Classify websites
df[['group', 'host']] = df['Website'].apply(classify_website)

# Save result
output_file = f"cleaned_{INPUT_FILE.rsplit('.', 1)[0]}.xlsx"
df.to_excel(output_file, index=False)

print(f" Done! Cleaned file saved as: {output_file}")

