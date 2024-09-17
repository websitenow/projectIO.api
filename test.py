import requests

prox = "https://project-io-api.vercel.app:8080"

proxies = {
    'http': prox,
    'https': prox,
}
response = requests.get('http://google.com', proxies=proxies)
print(response.text)