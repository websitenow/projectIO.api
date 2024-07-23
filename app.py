import requests
from re import findall, compile
from flask import Flask, request
from werkzeug.exceptions import HTTPException
from json import loads

app = Flask(__name__)

def get_captions(url):
    try:
        r = requests.get(url,timeout=5)
        if r.status_code == 200:
            html = r.text
            pdr = r'"captionTracks":\[\{(.*?)\}\]'
            pdr2 = r'http[a-z]:\/\/(.*?)\"'
            founds = findall(pdr, html)
            if len(founds) == 0:
                return
           
            founds = [loads('[{' + x.replace('\\u0026', '&') + '}]') for x in founds]
            founds = loads(str(founds)[1:-1])
            return founds
    except:
        pass
        
@app.route('/')
def GETcaptions():
    url = request.args.get('url')
    
    if url:
        captions = get_captions(url)
        captions = captions if captions else []
        return captions
    return []

@app.errorhandler(HTTPException)
def handle_bad_request(error):
    return f'bad request! {error.code}'

if __name__ == "__main__":
    app.run()
