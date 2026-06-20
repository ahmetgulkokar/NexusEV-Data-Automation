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
    
    if response.status_code != 200:
        print(f"Hata: Site {response.status_code} kodu döndürdü.")
        return

    try:
        data = response.json()
        # DEBUG: Sitenin bize ne gönderdiğini görmek için anahtarları yazdırıyoruz
        print("Gelen verinin anahtarları:", data.keys())
        # Eğer 'vehicles' yoksa, gelen verinin ilk 200 karakterini yazdıralım
        if 'vehicles' not in data:
            print("Uyarı: 'vehicles' anahtarı bulunamadı. Gelen veri örneği:")
            print(str(data)[:200])
            return
            
    except Exception as e:
        print(f"JSON parse hatası: {e}")
        return

    # Veriyi temizle
    vehicles = []
    for v in data.get('vehicles', []):
        vehicles.append({
            "brand": v.get('brand_name', 'Bilinmiyor'),
            "model": v.get('model_name', 'Bilinmiyor'),
            "image_url": v.get('image_url', ''),
            "avg_consumption": 16.0
        })
    
    # Gist güncelleme kısmı
    gist_id = os.environ['VEHICLE_GIST_ID']
    token = os.environ['GIST_TOKEN']
    headers_gist = {'Authorization': f'token {token}'}
    data_gist = {"files": {"vehicles.json": {"content": json.dumps(vehicles, ensure_ascii=False, indent=4)}}}
    
    update_res = requests.patch(f"https://api.github.com/gists/{gist_id}", headers=headers_gist, json=data_gist)
    
    if update_res.status_code == 200:
        print("Gist başarıyla güncellendi!")
    else:
        print(f"Gist güncelleme hatası: {update_res.status_code} - {update_res.text}")

if __name__ == "__main__":
    update_gist()
