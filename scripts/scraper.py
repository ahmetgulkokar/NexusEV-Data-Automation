import os
import requests
import json
from bs4 import BeautifulSoup

# Secret'lardan değerleri alıyoruz
GIST_ID = os.environ.get('GIST_ID')
GIST_TOKEN = os.environ.get('GIST_TOKEN')

def fetch_fuel_prices():
    # Petrol Ofisi Arşiv Sayfası
    url = "https://www.petrolofisi.com.tr/arsiv-fiyatlari"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Şimdilik örnek veri döndürüyoruz
    return {
        "2026-06": {"gasoline": 46.50, "diesel": 46.10},
        "2026-07": {"gasoline": 47.20, "diesel": 46.80}
    }

def update_gist(data):
    url = f"https://api.github.com/gists/{GIST_ID}"
    headers = {"Authorization": f"token {GIST_TOKEN}"}
    payload = {"files": {"fuel_prices.json": {"content": json.dumps(data, indent=4)}}}
    
    response = requests.patch(url, headers=headers, json=payload)
    if response.status_code == 200:
        print("Fiyatlar başarıyla güncellendi!")
    else:
        print(f"Hata: {response.status_code}")

if __name__ == "__main__":
    prices = fetch_fuel_prices()
    update_gist(prices)
