import os
import requests
import json
from bs4 import BeautifulSoup

GIST_ID = os.environ.get('GIST_ID')
GIST_TOKEN = os.environ.get('GIST_TOKEN')

def fetch_fuel_prices():
    url = "https://www.petrolofisi.com.tr/arsiv-fiyatlari"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Petrol Ofisi sayfasındaki tablo yapısını hedefliyoruz
    # Not: Tablonun class veya id bilgisi değişirse burayı güncellemek gerekir
    table = soup.find('table') 
    rows = table.find_all('tr')
    
    fuel_data = {}
    
    # Başlık satırını atlayıp verileri döngüye alıyoruz
    for row in rows[1:]:
        cols = row.find_all('td')
        if len(cols) >= 3:
            # Sütun yapısı: Tarih | Benzin | Motorin (Örnek)
            date = cols[0].text.strip()
            gasoline = float(cols[1].text.replace(',', '.').strip())
            diesel = float(cols[2].text.replace(',', '.').strip())
            
            fuel_data[date] = {"gasoline": gasoline, "diesel": diesel}
            
    return fuel_data

def update_gist(data):
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {"Authorization": f"token {GIST_TOKEN}"}
    payload = {"files": {"fuel_prices.json": {"content": json.dumps(data, indent=4)}}}
    
    response = requests.patch(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Gerçek veriler başarıyla Gist'e yazıldı!")
    else:
        print(f"Hata: {response.status_code}")

if __name__ == "__main__":
    prices = fetch_fuel_prices()
    update_gist(prices)
