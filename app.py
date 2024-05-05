from flask import Flask
from requests import get
from os import environ

app = Flask(__name__)

CONST = ['URL_1', 'URL_2']

@app.route("/")
def home():
    return "Hello!!!"

@app.route("/<index>/<name>")
def search(index, name):
    try:
        url = environ[CONST[int(index)]]
        html = get(url + name)
        return html.text
    except:
        return ":( <span style='color: red;'>Error</span>"

if __name__ == "__main__":
    app.run()
