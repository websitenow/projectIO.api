import requests
from re import findall, compile
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from json import loads, dumps

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
            res = ""
            for data in founds:
                res += '[{' + data.replace('\\u0026', '&').replace("'",'"') + '}]'
            return jsonify(res)
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
