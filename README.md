# Website Scraper

A Python + Playwright scraper for extracting offers data from the website.

The scraper collects:

- UUID
- Category
- Sub Category
- Merchant Name
- Offer Title
- Subtitle
- Summary
- Website
- Merchant Editorial
- Rules of Use
- Address
- City
- State
- Phone
- Latitude
- Longitude
- Detail URL

All results are exported into a CSV file.

---

# Features

- Automatic pagination (scrape all pages)
- Offer detail scraping
- Merchant editorial extraction
- Rules of use extraction
- Duplicate removal
- UTF-8 CSV export
- Single-offer testing mode
- Multiple region & category support

---

# Requirements

Install:

- Python 3.10+
- Google Chrome / Chromium

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/rifkykurniawan/ScraperToolForDD.Au.git
```

```bash
cd directory_name
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### macOS / Linux

Activate (Always activate the virtual environment):
```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install playwright
```

---

## 4. Install Playwright Browser

```bash
playwright install
```

---

# Run the Scraper

```bash
python scraper.py
```

---

# Output

The scraped data will be automatically saved as:

```bash
Informal_Dining_and_Takeaway.csv
```

---

# Configuration

## Regions

Edit this section:

```python
REGIONS = [
    "sydney",
]
```

Example:

```python
REGIONS = [
    "sydney",
    "melbourne",
    "brisbane",
]
```

---

## Categories

Edit this section:

```python
CATEGORIES = [
    "takeaway",
]
```

Example:

```python
CATEGORIES = [
    "cafe",
    "shopping",
    "activities",
    "travel",
]
```

---

## Pagination Limit

```python
LIMIT = 30
```

---

## Test One Offer Only

For quick testing:

```python
TEST_ONE_ONLY = True
```

To scrape all data:

```python
TEST_ONE_ONLY = False
```

---

# CSV Example

| uuid | category | sub_category | name | rules |
|---|---|---|---|---|
| xxx | Cafe and Family Dining | Japanese | Okami | • Rule 1 |

---

# Notes

- Rules of Use are separated line-by-line in the CSV
- Merchant Editorial is extracted from the offer detail page
- The scraper uses Playwright headless browser automation
- Duplicate UUIDs are automatically removed

---

# Troubleshooting

## Playwright browser missing

Run:

```bash
playwright install
```

---

## ModuleNotFoundError

Install dependencies:

```bash
pip install playwright
```

---

## CSV Permission Error

Make sure the CSV file is not currently opened in Excel or CSV Viewer Online.

---

# Tech Stack

- Python
- Playwright
- AsyncIO
- CSV Export

---

# Disclaimer

This project is intended for educational and data extraction research purposes only.

Please use responsibly and comply with the target website's Terms of Service.