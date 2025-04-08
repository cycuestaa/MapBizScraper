# MapBizScraper
A simple script to get business details from google maps into a spreadsheet. Freeeee

# 🧼 Business Scraper

This Python project automates the collection of beauty business data (e.g., salons, spas, barbers) using the **Google Maps Places API** based on ZIP codes. The goal is to support the Quila Beauty platform's outreach and onboarding efforts by efficiently gathering high-quality contact information.

---

## 🚀 Features

- Searches multiple ZIP codes
- Matches multiple search terms (e.g., “nail salon”, “hair stylist”)
- Collects:
  - Business name
  - Address
  - Phone number
  - Website
  - Business status
  - Google Maps URL
  - Matching search terms
  - Note: Email addresses are not returned by Google’s API (privacy restricted).
- Removes duplicates using Place ID
- Saves results into a clean Excel file

---

## 📦 Requirements 

- Python 3.x
- A Google Cloud project with:
  - **Places API** and **Geocoding API** enabled
  - An API key with usage rights

---

## 🧰 Installation

### 1. Clone this repository:
```bash
git clone https://github.com/your-username/quila-beauty-scraper.git
cd quila-beauty-scraper
```
### 2. Install Dependecies
```bash
pip install requests pandas openpyxl
```
### 3. Add your Google API Key
Open business_scraper.py and replace:
API_KEY = 'YOUR_API_KEY'

### 4. Usage
Update the following lists in the script:

```python
ZIP_CODES = ['90210', '10001']
SEARCH_TERMS = ["nail salon", "hair stylist", "medspa", "barber", "spa"]
RADIUS = 1609  # 1 mile in meters
```

### 5. Output
An Excel file named:
```python
df = pd.DataFrame(data)
df.to_excel("beauty_businesses_filtered.xlsx", index=False)
print("✅ Done! File saved as beauty_businesses_filtered.xlsx")
```


## To run the script:
beauty_businesses_filtered.xlsx
```bash
python business_scraper.py
```



## 🧠 Next Steps...

### 1. Build an Email Scraper from Website URLs
You can create a simple Python script that:

- Opens each business website URL from your Excel file
- Scans the HTML for email addresses using regex
- Saves the matched email addresses in a new column

#### Install Dependecies
pip install requests beautifulsoup4

### 2. Scrape and store social media URLs
For: Instagram, Facebook, Pinterest, TikTok, Twitter/X
- Adds a column for each platform
- Adds a boolean column to flag if any social media was found
  
