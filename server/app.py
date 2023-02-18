from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def test():
    return "<p>Hello, test!</p>"

@app.route("/test2")
def test2():
    return "<p>Hello, test2!</p>"
