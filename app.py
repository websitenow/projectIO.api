import requests as rq
from re import findall, compile
from flask import Flask, request, jsonify, render_template
from werkzeug.exceptions import HTTPException
from json import loads, dumps
from os import environ

app = Flask(__name__)

@app.route("/")
def homepage():
    return "<h2>HOMEPAGE</h2><br><a href='/proxy'>ACTIVE PROXYE</a>"

@app.route('/proxy')
def proxy():
   actived = environ.get("PROXYE_ACTIVED")
   return render_template("uploadproxye.html", actived=actived)

@app.route("/active")
def active_proxie():
    actived = environ.get("PROXYE_ACTIVED")
    if actived == "False":
        return "NOT ACTIVED"
    else:
       return "ACTIVED"

@app.route('/html')
def gethtml():
    try:
        url = request.args.get('url')
        html = rq.get(url)
        return html.text 
    except:
        return "<h1>Error</h1>"

@app.errorhandler(HTTPException)
def handle_bad_request(error):
   return f'bad request! {error.code}'

if __name__ == "__main__":
   app.run()
