from flask import Flask, render_template, request
import sqlite3
from cs50 import SQL

app = Flask(__name__)


db = SQL("sqlite:///cocktails.db")


@app.route("/")
def index():
    
  return render_template("index.html")


@app.route("/search")
def search():
    cocktails = db.execute("SELECT * FROM cocktails WHERE strDrink LIKE ? ORDER BY strDrink", "%" + request.args.get("q") + "%")


    return render_template("search.html", cocktails=cocktails)

