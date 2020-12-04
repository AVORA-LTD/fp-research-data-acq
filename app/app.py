import requests
import json

url = "https://anomaly-detection-v2.avora.com/anomaly_detection/anomaly_id/"
payload = {"ids":[], "n_jobs":1}

response = requests.post(url, data=json.dumps(payload))

print(str(response))