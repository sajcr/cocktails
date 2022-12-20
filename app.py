from flask import Flask, render_template, request
import sqlite3
from cs50 import SQL

app = Flask(__name__)


db = SQL("sqlite:///cocktails.db")


@app.route("/")
def index():
  
  cocktails = db.execute("SELECT idDrink, strDrink FROM cocktails")
  
  if request.args.get("idDrink"):
    idDrink = request.args.get("idDrink")
    
    drink = db.execute("SELECT * FROM cocktails WHERE idDrink = ?", idDrink)[0]
   
    ingredients = []
     
    for n in range(drink['numIngredients']):
      
      item = {
        "ingredient":drink[f"strIngredient{n+1}"],
        "measure":drink[f"strMeasure{n+1}"]
      }
    
      ingredients.append(item)
    
    
    
  return render_template("index.html", cocktails=cocktails, drink=drink, ingredients=ingredients)


"""
@app.route("/search")
def search():
  cocktails = db.execute("SELECT * FROM cocktails WHERE strDrink LIKE ? ORDER BY strDrink", "%" + request.args.get("q") + "%")
  return render_template("search.html", cocktails=cocktails)
"""

#@app.route("/retrieve",methods=["POST"])
#def retrieve():
#  id = request.form.get()
  
