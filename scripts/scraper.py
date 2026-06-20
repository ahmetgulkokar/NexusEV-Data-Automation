import os
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

GIST_ID = os.environ.get('GIST_ID')
GIST_TOKEN = os.environ.get('GIST_TOKEN')

def fetch_fuel_prices():
    url = "https://www.petrolofisi.com.tr/arsiv-fiyatlari"
    
    # Payload verilerini senin verdiğin bilgilerle güncelledik
    # Tarihleri otomatik olarak son 20 gün aralığına set edelim
    end_date = datetime.now().strftime('%d/%m/%Y')
    start_date = (datetime.now() - timedelta(days=20)).strftime('%d/%m/%Y')
    
    payload = {
        'template': '3',
        'cityId': '34',      # İstanbul
        'districtId': '03429', # Bağcılar
        'startDate': start_date,
        'endDate': end_date,
        'isBp': 'false'
    }
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # POST isteği ile veriyi gönderiyoruz
    response = requests.post(url, data=payload, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = soup.find('table', {'class': 'table-prices'})
    if not table:
        return {}
    
    rows = table.find_all('tr')
    fuel_data = {}
    
    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) > 1:
            date = cols[0].text.strip()
            # Fiyatları span içindeki 'with-tax' sınıfından alıyoruz
            prices = [p.text.strip() for p in cols[1].find_all('span', {'class': 'with-tax'})]
            fuel_data[date] = prices
            
    return fuel_data

def update_gist(data):
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {"Authorization": f"token {GIST_TOKEN}"}
    payload = {"files": {"fuel_prices.json": {"content": json.dumps(data, indent=4)}}}
    requests.patch(url, headers=headers, json=payload)

if __name__ == "__main__":
    prices = fetch_fuel_prices()
    update_gist(prices)
