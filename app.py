from flask import Flask, url_for, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    test = "flask"
    return render_template("index.html", secret=test)