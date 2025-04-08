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
