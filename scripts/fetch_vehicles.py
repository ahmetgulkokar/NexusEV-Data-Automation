import requests
import json
import os

def fetch_vehicles():
    # Site adresi
    url = "https://dolubatarya.com/araba?vehicle_types=1,2,3,4,5&in_tr=yes"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        vehicles = []
        
        # Sitenin döndürdüğü yapıya göre temizleme (Örnek modelleme)
        for item in data.get('vehicles', []):
            vehicles.append({
                "brand": item.get('brand_name'),
                "model": item.get('model_name'),
                "image_url": item.get('image_url'),
                "avg_consumption": 16.0 # Varsayılan değer
            })
            
        return vehicles
    return []

# Gist Güncelleme fonksiyonunu yakıt fiyatlarındaki gibi kullanacağız
