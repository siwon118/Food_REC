import requests
import uuid
import time
import json

api_url = 'https://hrksxbmwcd.apigw.ntruss.com/custom/v1/30071/9605970d2db830c95f3b3706dbc6fd8df47bcdbb0f43c096830176b5eb6baa33/general'
secret_key = 'VmNpYm1pUE9sZFNlZ3pha3VLYUhCV1hpYmFka2RrVWo='
image_file = 'C:/Users/hyeon/Downloads/abc.jpg'

request_json = {
    'images': [
        {
            'format': 'jpg',
            'name': 'demo'
        }
    ],
    'requestId': str(uuid.uuid4()),
    'version': 'V2',
    'timestamp': int(round(time.time() * 1000))
}

payload = {'message': json.dumps(request_json).encode('UTF-8')}
files = [
  ('file', open(image_file,'rb'))
]
headers = {
  'X-OCR-SECRET': secret_key
}

response = requests.request("POST", api_url, headers=headers, data=payload, files=files)
s1 = []
s2 = ""
allergy = ['계란', '우유', '밀', '갑각류', '생선', '호두', '돼지고기', '땅콩', '조개', '복숭아']
state = 0
for i in response.json()['images'][0]['fields']:
    text = i['inferText']
    s2+=text
    s1.append(text)
print(s1)
print(s2)
