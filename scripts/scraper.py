import os
import requests
import json
from bs4 import BeautifulSoup

GIST_ID = os.environ.get('GIST_ID')
GIST_TOKEN = os.environ.get('GIST_TOKEN')

def fetch_fuel_prices():
    # Senin verdiğin URL
    url = "https://www.tppd.com.tr/gecmis-akaryakit-fiyatlari?id=34&county=413&StartDate=01.06.2024&EndDate=21.06.2026"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Sayfadaki tabloyu bul (TPPD sitesindeki tablo yapısına göre)
    table = soup.find('table')
    if not table:
        return {"error": "Tablo bulunamadı"}
    
    rows = table.find_all('tr')
    fuel_data = {}
    
    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) >= 3:
            date = cols[0].text.strip()
            # Fiyat verilerini hücreden alıyoruz
            gasoline = cols[1].text.strip()
            diesel = cols[2].text.strip()
            fuel_data[date] = {"gasoline": gasoline, "diesel": diesel}
            
    return fuel_data

def update_gist(data):
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {"Authorization": f"token {GIST_TOKEN}"}
    payload = {"files": {"fuel_prices.json": {"content": json.dumps(data, indent=4)}}}
    requests.patch(url, headers=headers, json=payload)

if __name__ == "__main__":
    prices = fetch_fuel_prices()
    update_gist(prices)
