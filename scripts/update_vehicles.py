import requests
import json
import os

def update_gist():
    # Tarayıcı gibi davranmak için headers ekledik
    url = "https://dolubatarya.com/araba?vehicle_types=1,2,3,4,5&in_tr=yes"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    # Debug için yanıtı kontrol edelim
    if response.status_code != 200:
        print(f"Hata: Site {response.status_code} kodu döndürdü.")
        return

    try:
        data = response.json()
    except:
        print("Gelen yanıt JSON formatında değil. Gelen ham veri:")
        print(response.text[:500]) # İlk 500 karakteri yazdırıp sorunu görelim
        return

    # İşleme devam et...
    vehicles = [{"brand": v['brand_name'], "model": v['model_name'], "image_url": v['image_url'], "avg_consumption": 16.0} for v in data['vehicles']]
    
    # ... (Gist gönderme kısmı aynı kalacak)
