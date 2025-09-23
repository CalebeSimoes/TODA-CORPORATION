from flask import render_template
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/insight")
def insight():
    return render_template("insight.html")

if __name__ == '__main__':
    app.run(debug=True)