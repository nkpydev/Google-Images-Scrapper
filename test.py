import requests

url = 'http://google.com'

r = requests.get(url)

print(r.text)