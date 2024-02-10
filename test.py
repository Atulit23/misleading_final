import requests

api_url = 'http://127.0.0.1:5000/api/scrape'  

url_to_scrape = 'https://www.amazon.com/HP-Students-Business-Quad-Core-Storage/dp/B0B2D77YB8/ref=sr_1_5'

payload = {'url': url_to_scrape}

response = requests.post(api_url, json=payload)

if response.status_code == 200:
    result = response.json()

    print("Product Title:", result.get('title'))
    print("Product Description:", result.get('description'))
else:
    print("Error:", response.text)