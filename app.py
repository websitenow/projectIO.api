from flask import Flask
from requests import get

app = Flask(__name__)

GOOGLEURL = "https://www.google.com/search?tbm=isch&q="

@app.route("/<name>")
def homepage(name):
    try:
        html = get(GOOGLEURL + name)
        return html.text.replace('"/', '"https://www.google.com/')
    except:
        return ":( <span style='color: red;'>Error</span>"

if __name__ == "__main__":
    app.run()
