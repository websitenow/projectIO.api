from flask import Flask

app = Flask(__name__)

@app.route("/")
def homepage():
    return "Hello A<span style='color: red;'>PY</span>"

if __name__ == "__main__":
    app.run()