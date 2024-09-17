import requests
from re import findall, compile
from flask import Flask, request, jsonify, render_template
from werkzeug.exceptions import HTTPException
from json import loads, dumps
from os import environ
import subprocess
from threading import Thread

app = Flask(__name__)
global proxie
proxie = None

def startProxie():
    try:
        # Iniciar o subprocesso e redirecionar a saída para logs
        process = subprocess.Popen(
            ["proxy", "--hostname", "0.0.0.0", "--port", "8080"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print("Proxy started with PID: %d", process.pid)
        environ["PROXYE_ACTIVED"] = "True"
    except Exception as e:
        print("Failed to start proxy: %s", e)
        environ["PROXYE_ACTIVED"] = "False"

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