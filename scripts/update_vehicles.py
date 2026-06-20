import requests
import json
import os

def update_gist():
    url = "https://dolubatarya.com/araba?vehicle_types=1,2,3,4,5&in_tr=yes"
    
    # Senin tarayıcından kopyaladığımız "gerçek" tarayıcı kimliği
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36',
        'Referer': 'https://dolubatarya.com/araba?vehicle_types=1,2,3,4,5&in_tr=yes',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json, text/javascript, */*; q=0.01'
    }
    
    # Sitenin bizi tanımaması için bir de Session açalım
    session = requests.Session()
    session.headers.update(headers)
    
    response = session.get(url)
    
    # Veriyi alıp temizle (Burası sitenin HTML/JSON yapısına göre değişecek)
    # Eğer bu da boş dönerse, site veriyi dinamik JavaScript ile çekiyor demektir.
    print("Yanıt kodu:", response.status_code)
    print("Yanıt içeriği:", response.text[:200]) # İlk 200 karakteri görelim

    # ... (Geri kalan kısım aynı)
