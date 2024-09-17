import requests

prox = "https://project-io-api.vercel.app:9000"

proxies = {
    'http': prox,
    'https': prox,
}
response = requests.get('http://google.com', proxies=proxies)
print(response.text)