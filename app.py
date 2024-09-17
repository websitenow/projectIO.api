import requests
from re import findall, compile
from flask import Flask, request, jsonify, render_template
from werkzeug.exceptions import HTTPException
from json import loads, dumps
from os import environ
from subprocess import Popen
from threading import Thread

app = Flask(__name__)
global proxie
proxie = None

import subprocess
import logging

def startProxie():
    try:
        # Iniciar o subprocesso e redirecionar a saída para logs
        process = subprocess.Popen(
            ["proxy", "--hostname", "0.0.0.0", "--port", "8080"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logging.info("Proxy started with PID: %d", process.pid)
    except Exception as e:
        logging.error("Failed to start proxy: %s", e)

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
        try: 
            proxie.join()
        except:
            pass
        proxie = Thread(target=startProxie)
        proxie.start()
        return "NOT ACTIVED"
    else:
       return "ACTIVED"

@app.errorhandler(HTTPException)
def handle_bad_request(error):
   return f'bad request! {error.code}'

if __name__ == "__main__":
   app.run()