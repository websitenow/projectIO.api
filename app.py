import requests
from re import findall, compile
from flask import Flask, request, jsonify, render_template
from werkzeug.exceptions import HTTPException
from json import loads, dumps
from os import environ
import subprocess
from threading import Thread


import time
from typing import Any, Optional

from proxy import Proxy
from proxy.core.base import BaseTcpTunnelHandler
from proxy.http.responses import (
    PROXY_TUNNEL_UNSUPPORTED_SCHEME, PROXY_TUNNEL_ESTABLISHED_RESPONSE_PKT,
)

app = Flask(__name__)
global proxie
proxie = None


class HttpsConnectTunnelHandler(BaseTcpTunnelHandler):
    """A https CONNECT tunnel."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def handle_data(self, data: memoryview) -> Optional[bool]:
        # Queue for upstream if connection has been established
        if self.upstream and self.upstream._conn is not None:
            self.upstream.queue(data)
            return None

        # Parse client request
        self.request.parse(data)

        # Drop the request if not a CONNECT request
        if not self.request.is_https_tunnel:
            self.work.queue(PROXY_TUNNEL_UNSUPPORTED_SCHEME)
            return True

        # CONNECT requests are short and we need not worry about
        # receiving partial request bodies here.
        assert self.request.is_complete

        # Establish connection with upstream
        self.connect_upstream()

        # Queue tunnel established response to client
        self.work.queue(PROXY_TUNNEL_ESTABLISHED_RESPONSE_PKT)

        return None

def startProxie():
    # This example requires `threadless=True`
    with Proxy(
        work_klass=HttpsConnectTunnelHandler,
        threadless=True,
        port=8080,
    ):
        try:
            while True:
                print("PROXY ACTIVE")
                environ["PROXYE_ACTIVED"] = "True"
                time.sleep(1)
        except KeyboardInterrupt:
            environ["PROXYE_ACTIVED"] = "False"
            pass
    # try:
    #     # Iniciar o subprocesso e redirecionar a saída para logs
    #     process = subprocess.Popen(
    #         ["proxy", "--hostname", "0.0.0.0", "--port", "8080"],
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.PIPE
    #     )
    #     print("Proxy started with PID: %d", process.pid)
    #     environ["PROXYE_ACTIVED"] = "True"
    # except Exception as e:
    #     print("Failed to start proxy: %s", e)
    #     environ["PROXYE_ACTIVED"] = "False"

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