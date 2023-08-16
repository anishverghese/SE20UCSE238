import requests
from flask import Flask, request, jsonify
import time
import gevent.monkey

gevent.monkey.patch_all()

app = Flask(__name__)

def fetch_numbers_from_url(url):
    try:
        response = requests.get(url, timeout=0.5)
        if response.status_code == 200:
            data = response.json()
            return data.get("numbers", [])
    except requests.exceptions.Timeout:
        print(f"Timeout for URL: {url}")
    except Exception as e:
        print(f"Error fetching data from URL {url}: {e}")
    return []

@app.route('/numbers', methods=['GET'])
def get_numbers():
    urls = request.args.getlist('url')
    unique_numbers = set()
    
    jobs = [gevent.spawn(fetch_numbers_from_url, url) for url in urls]
    gevent.joinall(jobs)
    
    for job in jobs:
        numbers = job.value
        unique_numbers.update(numbers)
    
    response_data = {
        "numbers": sorted(list(unique_numbers))
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008)
