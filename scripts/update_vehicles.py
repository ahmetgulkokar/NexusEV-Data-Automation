import requests
import json
import os

def update_gist():
    # 1. Veriyi çek
    url = "https://dolubatarya.com/araba?vehicle_types=1,2,3,4,5&in_tr=yes"
    response = requests.get(url).json()
    vehicles = [{"brand": v['brand_name'], "model": v['model_name'], "image_url": v['image_url'], "avg_consumption": 16.0} for v in response['vehicles']]
    
    # 2. Gist'e gönder
    gist_id = os.environ['VEHICLE_GIST_ID']
    token = os.environ['GIST_TOKEN']
    headers = {'Authorization': f'token {token}'}
    data = {"files": {"vehicles.json": {"content": json.dumps(vehicles, ensure_ascii=False, indent=4)}}}
    
    requests.patch(f"https://api.github.com/gists/{gist_id}", headers=headers, json=data)

if __name__ == "__main__":
    update_gist()
